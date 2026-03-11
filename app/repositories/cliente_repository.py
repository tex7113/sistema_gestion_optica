from sqlalchemy.orm import Session, selectinload
from app.models.cliente_model import Cliente
from app.schemas.cliente_schema import ClienteCreate

class ClienteRepository:

    @staticmethod
    def get_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def get_cliente_by_id(db: Session, cliente_id:int):
        return db.query(Cliente).options(selectinload(Cliente.recetas)).filter(Cliente.id == cliente_id).first()

    @staticmethod
    def get_cliente_by_email(db: Session, cliente_email:str):
        return db.query(Cliente).filter(Cliente.correo_electronico == cliente_email).first()

    @staticmethod
    def create_cliente(db: Session, cliente: ClienteCreate, usuario_id:int):
        db_cliente = Cliente(**cliente.model_dump(), usuario_id = usuario_id)
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    @staticmethod
    def update_cliente(db: Session, cliente_id: int, cliente: ClienteCreate):
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not db_cliente:
            return None
        for key, value in cliente.model_dump(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    @staticmethod
    def delete_cliente(db: Session, cliente_id: int):
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not db_cliente:
            return None
        db_cliente.activo = False
        db.commit()
        db.refresh(db_cliente)
        return db_cliente