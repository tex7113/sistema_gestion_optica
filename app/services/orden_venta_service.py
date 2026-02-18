from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.orden_venta_repository import OrdenVentaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.receta_repository import RecetaRepository
from app.schemas.orden_venta_schema import OrdenVentaCreate, OrdenVentaUpdate

class OrdenVentaService:

    @staticmethod
    def listar(db: Session):
        return OrdenVentaRepository.get_all(db)

    @staticmethod
    def obtener_por_id(db: Session, orden_id: int):
        db_orden = OrdenVentaRepository.get_by_id(db, orden_id)

        if not db_orden:
            raise HTTPException(404, "Orden no encontrada")

        return db_orden

    @staticmethod
    def crear(db: Session, orden: OrdenVentaCreate):

        cliente = ClienteRepository.get_cliente_by_id(db, orden.cliente_id)
        if not cliente:
            raise HTTPException(404, "Cliente no existe")

        if orden.receta_id:
            receta = RecetaRepository.get_by_id(db, orden.receta_id)
            if not receta:
                raise HTTPException(404, "Receta no existe")

        return OrdenVentaRepository.create(db, orden)

    @staticmethod
    def actualizar(db: Session, orden_id: int, orden: OrdenVentaUpdate):
        db_orden = OrdenVentaRepository.get_by_id(db, orden_id)
        if not db_orden:
            raise HTTPException(404, "Orden no encontrada")

        if orden.receta_id:
            db_receta = RecetaRepository.get_by_id(db, orden.receta_id)
            if not db_receta:
                raise HTTPException(404, "Receta no existe")


        return OrdenVentaRepository.update(db, orden_id, orden)

    @staticmethod
    def eliminar(db: Session, orden_id: int):
        db_orden = OrdenVentaRepository.delete(db, orden_id)

        if not db_orden:
            raise HTTPException(404, "Orden no encontrada")

        return db_orden