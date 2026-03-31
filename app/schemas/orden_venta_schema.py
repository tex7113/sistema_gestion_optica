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
    usuario_id: int

    class Config:
        from_attributes = True


class OrdenVentaResumen(BaseModel):
    orden_id: int
    cliente_nombre: str
    cliente_telefono: str
    monto_total: Decimal
    total_abonado: Decimal
    saldo_pendiente: Decimal
    pagos_realizados: int
    pagos_pendientes: int | None
    estado_pago: str