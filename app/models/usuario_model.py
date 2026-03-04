from sqlalchemy import Boolean, Integer, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
import enum

class RolEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    VENDEDOR = "VENDEDOR"
    CAJA = "CAJA"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    correo_electronico: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    contrasenia: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[Enum] = mapped_column(Enum(RolEnum), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)