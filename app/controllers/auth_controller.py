from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth_schema import Login, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token)
def login(data: Login, db: Session = Depends(get_db)):
    return AuthService.login(db, data.correo_electronico, data.contrasenia)

@router.post("/token", response_model=Token)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login(db, form_data.username, form_data.password)

#Registrar Administrador
# @router.post("/registrar")
# def registrar(form_data: UsuarioCreate = Depends(), db: Session = Depends(get_db)):
#     return AuthService.registrar(db, form_data.username, form_data.password, "ADMIN")