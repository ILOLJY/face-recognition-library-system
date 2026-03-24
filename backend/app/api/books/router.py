"""图书相关路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.api.auth.dependencies import get_current_user
from app.models.users import User
from app.models.books import Book
from app.schemas.book import BookResponse, BookSimpleResponse
from app.cache.redis import get_redis

router = APIRouter()


@router.get("/recent", response_model=List[BookSimpleResponse], status_code=status.HTTP_200_OK)
async def get_recent_borrow_books(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取最近借阅的图书"""
    # 获取Redis客户端
    redis_client = await get_redis()
    
    # 从Redis List中获取最近10个图书ID
    recent_book_ids = await redis_client.redis.lrange("recent_borrow_books", 0, 9)
    
    # 转换为整数
    recent_book_ids = [int(book_id) for book_id in recent_book_ids if book_id]
    
    # 从数据库中获取图书信息
    from sqlalchemy import select
    result = await db.execute(select(Book).where(Book.id.in_(recent_book_ids)))
    books = result.scalars().all()
    
    # 按照Redis中的顺序排序
    book_dict = {book.id: book for book in books}
    sorted_books = [book_dict[book_id] for book_id in recent_book_ids if book_id in book_dict]
    
    # 如果不足10本，从数据库中补充
    if len(sorted_books) < 10:
        # 计算还需要多少本
        needed_count = 10 - len(sorted_books)
        
        # 从数据库中查询Redis中不存在的图书，按ID降序排列（最新的在前面）
        existing_ids = set(recent_book_ids)
        result = await db.execute(
            select(Book)
            .where(~Book.id.in_(existing_ids))
            .order_by(Book.id.desc())
            .limit(needed_count)
        )
        additional_books = result.scalars().all()
        
        # 添加到结果中
        sorted_books.extend(additional_books)
    
    return sorted_books
