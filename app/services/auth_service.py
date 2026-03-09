from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:

    @staticmethod
    def login(db: Session, usuario_email: str, contrasenia: str):
        db_usuario = UsuarioRepository.get_by_email(db, usuario_email)

        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        if not verify_password(contrasenia, db_usuario.contrasenia):
            raise HTTPException(status_code=401, detail="Credenciales invalidas")

        token = create_access_token({
            "sub": db_usuario.id,
            "email": db_usuario.correo_electronico,
            "rol": db_usuario.rol
        })

        return {
            "access_token": token,
            "token__type": "bearer"
        }

#Registrar Administrador
    # @staticmethod
    # def registrar(db: Session, usuario_email: str, contrasenia: str, rol: str):
    #     db_usuario = UsuarioRepository.get_by_email(db, usuario_email)
    #     if db_usuario:
    #         raise HTTPException(status_code=404, detail="El correo electronico ya esta en uso")
    #
    #     contrasenia_segura = hash_password(contrasenia)
    #
    #     return UsuarioRepository.create_admin(db, usuario_email, contrasenia_segura, rol)