from datetime import date
from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, Numeric, String, Date, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class PlanPago(Base):
    __tablename__ = "planes_pago"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    orden_venta_id: Mapped[int] = mapped_column(
        ForeignKey(
            "ordenes_venta.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True,
        index=True
    )
    numero_plazos: Mapped[int] = mapped_column(Integer, nullable=False)
    frecuencia: Mapped[str] = mapped_column(String(20), nullable=False)
    monto_parcial_sugerido: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)

    __table_args__ = (
        CheckConstraint("numero_plazos > 0", name="chk_numero_plazos"),
        CheckConstraint("monto_parcial_sugerido >= 0", name="chk_monto_parcial"),
    )

    #Relaciones

    orden = relationship("OrdenVenta", back_populates="plan_pago")