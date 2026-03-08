from pydantic import BaseModel, EmailStr
from app.models.usuario_model import RolEnum
from datetime import datetime

class UsuarioBase(BaseModel):
    correo_electronico: EmailStr
    nombre_completo: str
    rol: RolEnum

class UsuarioCreate(UsuarioBase):
    contrasenia: str

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True