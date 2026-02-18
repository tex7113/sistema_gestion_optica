from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.receta_repository import RecetaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.receta_schema import RecetaCreate, RecetaUpdate


class RecetaService:

    @staticmethod
    def listar(db: Session):
        return RecetaRepository.get_all(db)

    @staticmethod
    def obtener(db: Session, receta_id: int):
        receta = RecetaRepository.get_by_id(db, receta_id)

        if not receta:
            raise HTTPException(404, "Receta no encontrada")

        return receta

    @staticmethod
    def obtener_por_cliente_id(db: Session, cliente_id: int):
        receta = RecetaRepository.get_by_cliente(db, cliente_id)

        if not receta:
            raise HTTPException(404, "Receta no encontrada")

        return receta

    @staticmethod
    def crear(db: Session, receta: RecetaCreate):

        cliente = ClienteRepository.get_cliente_by_id(db, receta.cliente_id)

        if not cliente:
            raise HTTPException(404, "Cliente no existe")

        return RecetaRepository.create(db, receta)

    @staticmethod
    def actualizar(db: Session, receta_id: int, receta: RecetaUpdate):
        db_receta = RecetaRepository.update(db, receta_id, receta)

        if not db_receta:
            raise HTTPException(404, "Receta no encontrada")

        return db_receta

    @staticmethod
    def eliminar(db: Session, receta_id: int):
        db_receta = RecetaRepository.delete(db, receta_id)

        if not db_receta:
            raise HTTPException(404, "Receta no encontrada")

        return db_receta
