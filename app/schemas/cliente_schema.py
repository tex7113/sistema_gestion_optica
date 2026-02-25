from typing import List

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from app.schemas.receta_schema import RecetaResponse

class ClienteBase(BaseModel):
    nombre_completo: str
    correo_electronico: EmailStr
    telefono: str


class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True

class ClienteDetailResponse(ClienteResponse):
    recetas: List[RecetaResponse] = []