from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioCreate
from app.models.usuario_model import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import hash_password


class UsuarioService:

    @staticmethod
    def listar_usuarios(db: Session):
        return UsuarioRepository.get_usuarios(db)

    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int):
        db_usuario = UsuarioRepository.get_by_id(db, usuario_id)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail=f"usuario con id:{usuario_id} no encontrado")
        return db_usuario

    @staticmethod
    def obtener_por_correo(db: Session, usuario_email:str):
        db_usuario = UsuarioRepository.get_by_email(db, usuario_email)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="usuario no encontrado")
        return db_usuario

    @staticmethod
    def crear_usuario(db: Session, usuario):

        if UsuarioRepository.get_by_email(db, usuario.correo_electronico):
            raise HTTPException(400, "El correo electronico ya está registrado")

        if UsuarioRepository.get_by_username(db, usuario.nombre_completo):
            raise HTTPException(400, "El nombre de usuario ya existe")

        db_usuario = Usuario(
            correo_electronico=usuario.correo_electronico,
            nombre_completo=usuario.nombre_completo,
            contrasenia=hash_password(usuario.contrasenia),
            rol=usuario.rol
        )

        return UsuarioRepository.create_user(db, db_usuario)

    @staticmethod
    def actualizar(db: Session, usuario_id: int, usuario: UsuarioCreate):
        db_usuario = UsuarioRepository.get_by_id(db, usuario_id)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail=f"usuario con id:{usuario_id} no encontrado")

        usuario_email = UsuarioRepository.get_by_email(db, usuario.correo_electronico)
        if usuario_email and usuario_email.id != usuario_id:
            raise HTTPException(status_code=400, detail="El correo electronico ya existe")

        db_username = UsuarioRepository.get_by_username(db, usuario.nombre_completo)
        if db_username and db_username.id != usuario_id:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

        return UsuarioRepository.update(db, usuario_id, usuario)


    @staticmethod
    def eliminar(db: Session, usuario_id: int):
        db_usuario = UsuarioRepository.desactivate(db, usuario_id)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail=f"usuario con id:{usuario_id} no encontrado")
        return db_usuario

    @staticmethod
    def activar(db: Session, usuario_id: int):
        db_usuario = UsuarioRepository.activate(db, usuario_id)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail=f"usuario con id:{usuario_id} no encontrado")
        return db_usuario