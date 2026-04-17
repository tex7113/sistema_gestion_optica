from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate
from datetime import datetime, timedelta

class ClienteService:

    @staticmethod
    def listar(db: Session, fecha_inicio = None, fecha_fin = None):

        if fecha_inicio is not None and fecha_fin is not None:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                fecha_fin= datetime.strptime(fecha_fin, "%Y-%m-%d").date() + timedelta(days=1)
            except ValueError:
                raise HTTPException(status_code=400, detail="valores incorrectos. Asegurese de mandar formato: YYYY-MM-DD")

        return ClienteRepository.get_clientes(db, fecha_inicio, fecha_fin)

    @staticmethod
    def obtener_por_id(db: Session, cliente_id: int):
        db_cliente = ClienteRepository.get_cliente_by_id(db, cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente con id:{cliente_id} no encontrado")
        return db_cliente

    @staticmethod
    def obtener_por_correo(db: Session, cliente_email:str):
        db_cliente = ClienteRepository.get_cliente_by_email(db, cliente_email)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return db_cliente

    @staticmethod
    def crear(db: Session, cliente: ClienteCreate, usuario_id: int):
        db_cliente = ClienteRepository.get_cliente_by_email(db, cliente.correo_electronico)
        if db_cliente:
            raise HTTPException(status_code=400, detail="El cliente ya existe")
        return ClienteRepository.create_cliente(db, cliente, usuario_id)

    @staticmethod
    def actualizar(db: Session, cliente_id: int, cliente: ClienteCreate):
        db_cliente = ClienteRepository.get_cliente_by_id(db, cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente con id:{cliente_id} no encontrado")

        cliente_email = ClienteRepository.get_cliente_by_email(db, cliente.correo_electronico)
        if cliente_email and cliente_email.id != cliente_id:
            raise HTTPException(status_code=400, detail="El correo electronico ya existe")
        return ClienteRepository.update_cliente(db, cliente_id, cliente)


    @staticmethod
    def eliminar(db: Session, cliente_id: int):
        db_cliente = ClienteRepository.delete_cliente(db, cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente con id:{cliente_id} no encontrado")
        return db_cliente

    @staticmethod
    def activar(db: Session, cliente_id: int):
        db_cliente = ClienteRepository.activate_cliente(db, cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente con id:{cliente_id} no encontrado")
        return db_cliente