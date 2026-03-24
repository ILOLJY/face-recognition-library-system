"""借阅相关的 Pydantic schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BorrowCreate(BaseModel):
    """创建借阅请求模型"""
    book_id: int = Field(..., description="图书ID")


class BorrowResponse(BaseModel):
    """借阅响应模型"""
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str
    renew_count: int
    fine_amount: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
