from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field


TipoPago = Literal["CONTADO", "CREDITO"]
EstadoPago = Literal["PENDIENTE", "PAGADO"]


class OrdenVentaBase(BaseModel):
    cliente_id: int
    receta_id: Optional[int] = None

    monto_total: Decimal = Field(ge=0)

    tipo_pago: TipoPago
    estado_pago: EstadoPago = "PENDIENTE"


class OrdenVentaCreate(OrdenVentaBase):
    pass


class OrdenVentaUpdate(BaseModel):
    receta_id: Optional[int] = None
    monto_total: Optional[Decimal] = Field(None, ge=0)
    tipo_pago: Optional[TipoPago] = None
    estado_pago: Optional[EstadoPago] = None


class OrdenVentaResponse(OrdenVentaBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
