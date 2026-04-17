from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate


class UsuarioRepository:

    @staticmethod
    def get_usuarios(db: Session):
        return db.query(Usuario).all()

    @staticmethod
    def get_by_email(db: Session, email:str):
        db_user = db.query(Usuario).filter(Usuario.correo_electronico == email).first()
        return db_user

    @staticmethod
    def get_by_id(db: Session, usuario_id:int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()


    @staticmethod
    def get_by_username(db: Session, user_name):
        return db.query(Usuario).filter(Usuario.nombre_completo == user_name).first()

    @staticmethod
    def create(db: Session, usuario: Usuario):
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def update(db:Session, usuario_id: int, usuario: UsuarioCreate):
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not db_usuario:
            return None
        for key, value in usuario.model_dump(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def desactivate(db: Session, usuario_id: int):
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not db_usuario:
            return None
        db_usuario.activo = False
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def activate(db:Session, usuario_id: int):
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not db_usuario:
            return None
        db_usuario.activo = True
        db.commit()
        db.refresh(db_usuario)
        return db_usuario



#Crear Administradores
    # @staticmethod
    # def create_admin(db: Session, email: str, password: str, rol: str):
    #     db_usuario = Usuario(
    #         correo_electronico=email,
    #         contrasenia=password,
    #         rol=rol,
    #         nombre_completo = "Admin"
    #     )
    #     db.add(db_usuario)
    #     db.commit()
    #     db.refresh(db_usuario)
    #     return db_usuario