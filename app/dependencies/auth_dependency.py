from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from app.repositories.usuario_repository import UsuarioRepository
from app.core.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(401, "Token inválido")

    user_id = payload.get("sub")

    usuario = UsuarioRepository.get_by_id(db, user_id)

    if not usuario:
        raise HTTPException(401, "Usuario no encontrado")

    return usuario


def require_role(roles: list):

    def role_checker(user=Depends(get_current_user)):
        if user.rol.value not in roles:
            print("hola 1")
            raise HTTPException(403, "No autorizado")
        print("hola 2")
        return user

    return role_checker