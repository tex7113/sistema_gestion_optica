from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    correo_electronico: EmailStr
    contrasenia: str

class Token(BaseModel):
    access_token: str
    token_type: str