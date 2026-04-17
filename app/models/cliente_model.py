from sqlalchemy import String, Integer, Boolean, TIMESTAMP, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(150))
    telefono: Mapped[str] = mapped_column(String(20))
    correo_electronico: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    fecha_registro: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(), nullable=False, index=True)
    activo: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    direccion: Mapped[str] = mapped_column(String(255), nullable=True)

    #Relacion
    #
    recetas = relationship("Receta", back_populates="cliente", cascade="all, delete-orphan")
    ordenes_venta = relationship("OrdenVenta", back_populates="cliente")
    usuario = relationship("Usuario", back_populates="clientes")