from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.usuario_schema import UsuarioCreate

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login(db, form_data.username, form_data.password)

#Registrar Administrador
# @router.post("/registrar")
# def registrar(form_data: UsuarioCreate = Depends(), db: Session = Depends(get_db)):
#     return AuthService.registrar(db, form_data.username, form_data.password, "ADMIN")