from fastapi import HTTPException
from app.models.usuario_model import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import hash_password


class UsuarioService:

    @staticmethod
    def crear_usuario(db, usuario):

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

        return UsuarioRepository.create(db, db_usuario)