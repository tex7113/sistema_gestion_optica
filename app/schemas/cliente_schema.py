from pydantic import BaseModel, EmailStr
from datetime import datetime

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