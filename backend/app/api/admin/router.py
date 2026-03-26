"""管理员相关路由"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

from app.db.session import get_db
from app.api.auth.dependencies import get_current_user
from app.models.users import User, UserRole
from app.models.books import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse

router = APIRouter()


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取管理员用户"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无管理员权限"
        )
    return current_user


@router.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """获取所有图书"""
    from sqlalchemy import select
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """添加图书"""
    # 创建图书
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


@router.put("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book(
    book_id: int,
    book: BookUpdate,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """编辑图书"""
    # 查找图书
    from sqlalchemy import select
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 更新图书信息
    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(
    book_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """删除图书"""
    # 查找图书
    from sqlalchemy import select
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 删除图书
    await db.delete(db_book)
    await db.commit()
    
    return {"msg": "图书删除成功"}


@router.post("/books/{book_id}/cover", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def upload_book_cover(
    book_id: int,
    file: UploadFile = File(...),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """上传图书封面"""
    # 查找图书
    from sqlalchemy import select
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 确保上传目录存在
    upload_dir = "app/static/covers"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, f"{book_id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 更新图书封面路径
    db_book.cover_image = f"/static/covers/{book_id}_{file.filename}"
    await db.commit()
    await db.refresh(db_book)
    
    return db_book