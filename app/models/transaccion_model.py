from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, ForeignKey, Numeric, TIMESTAMP, Text, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Transaccion(Base):
    __tablename__ = "transacciones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    orden_venta_id: Mapped[int] = mapped_column(
        ForeignKey(
            "ordenes_venta.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    monto_abonado: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    metodo_pago: Mapped[str | None] = mapped_column(String(30))
    nota: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("monto_abonado > 0", name="chk_monto_abonado"),
    )

    #Relaciones
    orden = relationship("OrdenVenta", back_populates="transacciones")