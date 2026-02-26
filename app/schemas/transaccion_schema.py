from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

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

    class Config:
        from_attributes = True