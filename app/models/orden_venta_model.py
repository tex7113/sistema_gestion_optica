from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI
from sqlalchemy import Integer,ForeignKey,Numeric,String,TIMESTAMP,func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class OrdenVenta(Base):
    __tablename__ = "ordenes_venta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receta_id: Mapped[int | None] = mapped_column(ForeignKey("recetas.id", ondelete="SET NULL"), nullable=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=False, index=True)
    monto_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    tipo_pago: Mapped[str] = mapped_column(String(20), nullable=False)
    estado_pago: Mapped[str] = mapped_column(String(20), server_default="PENDIENTE", nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("monto_total >= 0", name="chk_monto_total"),
        CheckConstraint(
            "tipo_pago IN ('CONTADO','CREDITO')",
            name="chk_tipo_pago"
        ),
        CheckConstraint(
            "estado_pago IN ('PENDIENTE','PAGADO')",
            name="chk_estado_pago"
        ),
    )

    # Relaciones
    cliente = relationship("Cliente", back_populates="ordenes_venta")
    receta = relationship("Receta", back_populates="ordenes_venta")
    plan_pago = relationship("PlanPago", back_populates="orden", uselist=False, cascade="all, delete-orphan")
    transacciones = relationship("Transaccion", back_populates="orden", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="ordenes_venta")