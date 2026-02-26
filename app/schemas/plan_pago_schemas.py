from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class PlanPagoBase(BaseModel):
    orden_venta_id: int
    numero_plazos: int = Field(gt=0)
    frecuencia: str
    monto_parcial_sugerido: Decimal = Field(ge=0)
    fecha_inicio: date | None = None

class PlanPagoCreate(PlanPagoBase):
    pass

class PlanPagoResponse(PlanPagoBase):
    id: int

    class Config:
        from_attributes = True