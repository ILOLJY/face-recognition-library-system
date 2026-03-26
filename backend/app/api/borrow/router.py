"""借阅相关路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.api.auth.dependencies import get_current_user
from app.models.users import User
from app.models.books import Book, BookStatus
from app.models.borrow_records import BorrowRecord, BorrowStatus
from app.schemas.borrow import BorrowCreate, BorrowResponse
from app.cache.redis import get_redis

router = APIRouter()


@router.post("/borrow", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
async def borrow_book(
    borrow_data: BorrowCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """借阅图书"""
    # 查找图书
    from sqlalchemy import select
    result = await db.execute(select(Book).where(Book.id == borrow_data.book_id))
    book = result.scalar()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 检查图书是否可借阅
    if book.status != BookStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图书不可借阅"
        )
    
    # 检查可借阅数量
    if book.available_copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图书已无可用副本"
        )
    
    # 创建借阅记录
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book.id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14),  # 默认借阅14天
        status=BorrowStatus.BORROWED
    )
    
    # 更新图书状态
    book.status = BookStatus.BORROWED
    book.available_copies -= 1
    
    # 保存到数据库
    db.add(borrow_record)
    await db.commit()
    await db.refresh(borrow_record)
    
    # 为借阅记录添加图书信息
    borrow_record.book_title = book.title
    borrow_record.book_author = book.author
    
    # 更新Redis中的最近借阅图书列表
    redis_client = await get_redis()
    # 先删除旧的记录（去重）
    await redis_client.redis.lrem("recent_borrow_books", 0, str(book.id))
    # 添加到列表头部
    await redis_client.redis.lpush("recent_borrow_books", str(book.id))
    # 限制列表长度为100
    await redis_client.redis.ltrim("recent_borrow_books", 0, 99)
    
    return borrow_record


@router.post("/return/{record_id}", response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def return_book(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """归还图书"""
    # 查找借阅记录
    from sqlalchemy import select
    result = await db.execute(
        select(BorrowRecord).where(
            BorrowRecord.id == record_id,
            BorrowRecord.user_id == current_user.id,
            BorrowRecord.status.in_([BorrowStatus.BORROWED, BorrowStatus.OVERDUE, BorrowStatus.RENEWED])
        )
    )
    borrow_record = result.scalar()
    
    if not borrow_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="借阅记录不存在或已归还"
        )
    
    # 查找图书
    result = await db.execute(select(Book).where(Book.id == borrow_record.book_id))
    book = result.scalar()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 更新借阅记录
    borrow_record.return_date = datetime.utcnow()
    borrow_record.status = BorrowStatus.RETURNED
    
    # 更新图书状态
    book.status = BookStatus.AVAILABLE
    book.available_copies += 1
    
    # 保存到数据库
    await db.commit()
    await db.refresh(borrow_record)
    
    # 为借阅记录添加图书信息
    borrow_record.book_title = book.title
    borrow_record.book_author = book.author
    
    return borrow_record


@router.get("/records", response_model=List[BorrowResponse], status_code=status.HTTP_200_OK)
async def get_borrow_records(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的借阅记录"""
    from sqlalchemy import select
    # 关联查询获取图书信息
    result = await db.execute(
        select(BorrowRecord, Book.title, Book.author).join(
            Book, BorrowRecord.book_id == Book.id
        ).where(BorrowRecord.user_id == current_user.id)
    )
    
    records = []
    for borrow_record, book_title, book_author in result:
        # 为借阅记录添加图书信息
        borrow_record.book_title = book_title
        borrow_record.book_author = book_author
        records.append(borrow_record)
    
    return records


@router.post("/renew/{record_id}", response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def renew_book(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """续借图书"""
    # 查找借阅记录
    from sqlalchemy import select
    result = await db.execute(
        select(BorrowRecord).where(
            BorrowRecord.id == record_id,
            BorrowRecord.user_id == current_user.id,
            BorrowRecord.status.in_([BorrowStatus.BORROWED, BorrowStatus.OVERDUE])
        )
    )
    borrow_record = result.scalar()
    
    if not borrow_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="借阅记录不存在或已归还"
        )
    
    # 检查续借次数
    if borrow_record.renew_count >= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="续借次数已达上限"
        )
    
    # 更新借阅记录
    borrow_record.due_date += timedelta(days=14)  # 续借14天
    borrow_record.renew_count += 1
    borrow_record.status = BorrowStatus.RENEWED
    
    # 保存到数据库
    await db.commit()
    await db.refresh(borrow_record)
    
    # 获取图书信息
    result = await db.execute(select(Book).where(Book.id == borrow_record.book_id))
    book = result.scalar()
    
    # 为借阅记录添加图书信息
    borrow_record.book_title = book.title
    borrow_record.book_author = book.author
    
    return borrow_record
