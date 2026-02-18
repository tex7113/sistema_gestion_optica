"""Se actualizo el campo activo de clientes

Revision ID: 185d3fd1c230
Revises: 72667da9d432
Create Date: 2026-02-18 14:21:17.805755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '185d3fd1c230'
down_revision: Union[str, Sequence[str], None] = '72667da9d432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "clientes",
        "fecha_registro",
        existing_type=sa.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )

    op.alter_column(
        "clientes",
        "activo",
        existing_type=sa.BOOLEAN(),
        server_default=sa.text("true"),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "clientes",
        "fecha_registro",
        existing_type=sa.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=False,
    )

    op.alter_column(
        "clientes",
        "activo",
        existing_type=sa.BOOLEAN(),
        server_default=None,
        existing_nullable=False,
    )