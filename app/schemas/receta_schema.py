from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RecetaBase(BaseModel):
    cliente_id: int
    fecha_consulta: Optional[date] = None

    # OD
    od_esfera: Optional[float] = None
    od_cilindro: Optional[float] = None
    od_eje: Optional[int] = None
    od_adicion: Optional[float] = None

    # OI
    oi_esfera: Optional[float] = None
    oi_cilindro: Optional[float] = None
    oi_eje: Optional[int] = None
    oi_adicion: Optional[float] = None

    observaciones: Optional[str] = None
    recomendacion_lente: Optional[str] = None


class RecetaCreate(RecetaBase):
    pass


class RecetaUpdate(BaseModel):
    fecha_consulta: Optional[date] = None

    od_esfera: Optional[float] = None
    od_cilindro: Optional[float] = None
    od_eje: Optional[int] = None
    od_adicion: Optional[float] = None

    oi_esfera: Optional[float] = None
    oi_cilindro: Optional[float] = None
    oi_eje: Optional[int] = None
    oi_adicion: Optional[float] = None

    observaciones: Optional[str] = None
    recomendacion_lente: Optional[str] = None


class RecetaResponse(RecetaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
