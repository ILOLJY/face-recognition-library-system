import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class UserRole(enum.Enum):
    """用户角色枚举"""
    ADMIN = "admin"  # 管理员
    USER = "user"    # 普通用户


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="用户ID，主键")

    # 基本信息
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment="用户名，唯一")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码，加密存储")
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="邮箱地址，唯一")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像图片路径")

    # 权限与状态
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False, comment="用户角色：admin-管理员, user-普通用户")
    is_active: Mapped[bool] = mapped_column(default=True, comment="账号是否激活")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关系
    face_data: Mapped["FaceData"] = relationship("FaceData", back_populates="user", uselist=False, cascade="all, delete-orphan")
    borrow_records: Mapped[List["BorrowRecord"]] = relationship("BorrowRecord", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, role={self.role.value})>"
