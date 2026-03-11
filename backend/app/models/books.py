import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class BookStatus(enum.Enum):
    """图书状态枚举"""
    AVAILABLE = "available"  # 可借阅
    BORROWED = "borrowed"    # 已借出
    RESERVED = "reserved"    # 已预约
    DAMAGED = "damaged"      # 损坏
    LOST = "lost"            # 丢失


class Book(Base):
    """图书模型"""
    __tablename__ = "books"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="图书ID，主键")

    # 图书标识
    isbn: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True, nullable=True, comment="ISBN编号")

    # 图书信息
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True, comment="书名")
    author: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="作者")
    publisher: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="出版社")
    publish_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="出版日期")
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True, comment="图书分类")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="图书简介")
    cover_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图片路径")

    # 库存信息
    total_copies: Mapped[int] = mapped_column(Integer, default=1, comment="图书总册数")
    available_copies: Mapped[int] = mapped_column(Integer, default=1, comment="可借阅册数")
    location: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="存放位置")

    # 状态
    status: Mapped[BookStatus] = mapped_column(Enum(BookStatus), default=BookStatus.AVAILABLE, comment="图书状态")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关系
    borrow_records: Mapped[List["BorrowRecord"]] = relationship("BorrowRecord", back_populates="book")

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
