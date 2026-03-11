from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from app.schemas.orden_venta_schema import OrdenVentaResumen

class TransaccionBase(BaseModel):
    orden_venta_id: int
    monto_abonado: Decimal = Field(gt=0)
    metodo_pago: str | None = None
    nota: str | None = None

class TransaccionCreate(TransaccionBase):
    pass

class TransaccionResponse(TransaccionBase):
    id: int
    fecha_pago: datetime
    usuario_id: int

    class Config:
        from_attributes = True

class PagoResponse(BaseModel):
    transaccion: TransaccionResponse
    resumen_pago: OrdenVentaResumen