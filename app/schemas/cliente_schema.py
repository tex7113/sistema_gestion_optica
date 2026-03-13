from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from app.schemas.receta_schema import RecetaResponse

class ClienteBase(BaseModel):
    nombre_completo: str
    correo_electronico: EmailStr
    telefono: str
    edad: int|None = None
    direccion: str|None = None


class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    fecha_registro: datetime
    activo: bool
    usuario_id: int

    class Config:
        from_attributes = True

class ClienteDetailResponse(ClienteResponse):
    recetas: List[RecetaResponse] = []