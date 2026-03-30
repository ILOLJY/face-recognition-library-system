"""change face_encoding to json

Revision ID: 56df52294bb9
Revises: 6b44dfe627e1
Create Date: 2026-03-30 14:35:51.449449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '56df52294bb9'
down_revision: Union[str, None] = '6b44dfe627e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 删除旧字段（BYTEA）
    op.drop_column('face_data', 'face_encoding')

    # 2. 新建 JSON 字段
    op.add_column(
        'face_data',
        sa.Column(
            'face_encoding',
            sa.JSON(),
            nullable=False,
            comment='JSON格式人脸特征向量'
        )
    )


def downgrade() -> None:
    # 回滚：删 JSON → 恢复 BYTEA
    op.drop_column('face_data', 'face_encoding')

    op.add_column(
        'face_data',
        sa.Column(
            'face_encoding',
            postgresql.BYTEA(),
            nullable=False,
            comment='人脸特征向量，二进制存储'
        )
    )