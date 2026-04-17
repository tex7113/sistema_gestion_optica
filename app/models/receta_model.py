from datetime import date, datetime
from sqlalchemy import Integer,ForeignKey,Date,Numeric,Text,String,TIMESTAMP,func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="CASCADE"),nullable=False,index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=False, index=True)
    fecha_consulta: Mapped[date] = mapped_column(Date,server_default=func.current_date(), nullable=False)
    # Ojo Derecho
    od_esfera: Mapped[float | None] = mapped_column(Numeric(5, 2))
    od_cilindro: Mapped[float | None] = mapped_column(Numeric(5, 2))
    od_eje: Mapped[int | None] = mapped_column(Integer)
    od_adicion: Mapped[float | None] = mapped_column(Numeric(5, 2))
    # Ojo Izquierdo
    oi_esfera: Mapped[float | None] = mapped_column(Numeric(5, 2))
    oi_cilindro: Mapped[float | None] = mapped_column(Numeric(5, 2))
    oi_eje: Mapped[int | None] = mapped_column(Integer)
    oi_adicion: Mapped[float | None] = mapped_column(Numeric(5, 2))

    observaciones: Mapped[str | None] = mapped_column(Text)
    recomendacion_lente: Mapped[str | None] = mapped_column(String(100))
    fecha_creacion: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False, index=True)

    # Relación
    cliente = relationship("Cliente", back_populates="recetas")
    ordenes_venta = relationship("OrdenVenta", back_populates="receta")
    usuario = relationship("Usuario", back_populates="recetas")