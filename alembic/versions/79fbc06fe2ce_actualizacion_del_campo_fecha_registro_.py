"""actualizacion del campo fecha_registro de la tabla clientes

Revision ID: 79fbc06fe2ce
Revises: fbfd3291a8f1
Create Date: 2026-02-18 12:45:35.359537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '79fbc06fe2ce'
down_revision: Union[str, Sequence[str], None] = 'fbfd3291a8f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cambiar nombre de columna y tipo
    op.alter_column('clientes', 'nombre', new_column_name='nombre_completo', existing_type=sa.String(100))
    op.alter_column('clientes', 'email', new_column_name='correo_electronico', existing_type=sa.String(150))

    # Agregar fecha_registro si no existe
    op.add_column('clientes', sa.Column('fecha_registro', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

    # Agregar activo si no existe
    op.add_column('clientes', sa.Column('activo', sa.Boolean(), nullable=False, server_default='true'))

    # Eliminar constraint antiguo
    op.drop_constraint('clientes_email_key', 'clientes', type_='unique')


def downgrade() -> None:
    op.alter_column('clientes', 'nombre_completo', new_column_name='nombre', existing_type=sa.String(150))
    op.alter_column('clientes', 'correo_electronico', new_column_name='email', existing_type=sa.String(150))
    op.drop_column('clientes', 'fecha_registro')
    op.drop_column('clientes', 'activo')
    op.create_unique_constraint('clientes_email_key', 'clientes', ['email'])