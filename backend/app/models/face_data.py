from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class FaceData(Base):
    """人脸特征数据模型"""
    __tablename__ = "face_data"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="人脸数据ID，主键")

    # 外键关联
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        comment="关联的用户ID，外键"
    )

    # 人脸数据
    face_encoding: Mapped[bytes] = mapped_column(LargeBinary, nullable=False, comment="人脸特征向量，二进制存储")
    face_image_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="人脸照片存储路径")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="face_data")

    def __repr__(self) -> str:
        return f"<FaceData(id={self.id}, user_id={self.user_id})>"
