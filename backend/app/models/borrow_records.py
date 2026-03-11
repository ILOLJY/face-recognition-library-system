import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class BorrowStatus(enum.Enum):
    """借阅状态枚举"""
    BORROWED = "borrowed"  # 借阅中
    RETURNED = "returned"  # 已归还
    OVERDUE = "overdue"    # 逾期
    RENEWED = "renewed"    # 已续借


class BorrowRecord(Base):
    """借阅记录模型"""
    __tablename__ = "borrow_records"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="借阅记录ID，主键")

    # 外键关联
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="借阅用户ID，外键"
    )
    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        comment="借阅图书ID，外键"
    )

    # 借阅时间信息
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="借阅日期")
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="应还日期")
    return_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="实际归还日期")

    # 借阅状态
    status: Mapped[BorrowStatus] = mapped_column(
        Enum(BorrowStatus),
        default=BorrowStatus.BORROWED,
        nullable=False,
        comment="借阅状态：borrowed-借阅中, returned-已归还, overdue-逾期, renewed-已续借"
    )

    # 续借与罚款
    renew_count: Mapped[int] = mapped_column(Integer, default=0, comment="续借次数")
    fine_amount: Mapped[float] = mapped_column(default=0.0, comment="罚款金额")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注信息")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="borrow_records")
    book: Mapped["Book"] = relationship("Book", back_populates="borrow_records")

    def __repr__(self) -> str:
        return f"<BorrowRecord(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status.value})>"
