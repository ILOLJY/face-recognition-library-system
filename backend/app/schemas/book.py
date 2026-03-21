"""图书相关的 Pydantic schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    """创建图书请求模型"""
    title: str = Field(..., min_length=1, max_length=200, description="书名")
    author: str = Field(..., min_length=1, max_length=100, description="作者")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN编号")
    publisher: Optional[str] = Field(None, max_length=100, description="出版社")
    publish_date: Optional[datetime] = Field(None, description="出版日期")
    category: Optional[str] = Field(None, max_length=50, description="图书分类")
    description: Optional[str] = Field(None, description="图书简介")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图片路径")
    total_copies: int = Field(1, ge=1, description="图书总册数")
    available_copies: int = Field(1, ge=0, description="可借阅册数")
    location: Optional[str] = Field(None, max_length=50, description="存放位置")


class BookUpdate(BaseModel):
    """更新图书请求模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="书名")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="作者")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN编号")
    publisher: Optional[str] = Field(None, max_length=100, description="出版社")
    publish_date: Optional[datetime] = Field(None, description="出版日期")
    category: Optional[str] = Field(None, max_length=50, description="图书分类")
    description: Optional[str] = Field(None, description="图书简介")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图片路径")
    total_copies: Optional[int] = Field(None, ge=1, description="图书总册数")
    available_copies: Optional[int] = Field(None, ge=0, description="可借阅册数")
    location: Optional[str] = Field(None, max_length=50, description="存放位置")


class BookResponse(BaseModel):
    """图书响应模型"""
    id: int
    title: str
    author: str
    isbn: Optional[str]
    publisher: Optional[str]
    publish_date: Optional[datetime]
    category: Optional[str]
    description: Optional[str]
    cover_image: Optional[str]
    total_copies: int
    available_copies: int
    location: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
