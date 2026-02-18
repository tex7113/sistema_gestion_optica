from sqlalchemy.orm import Session

from app.models.orden_venta_model import OrdenVenta
from app.schemas.orden_venta_schema import OrdenVentaCreate, OrdenVentaUpdate


class OrdenVentaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(OrdenVenta).all()

    @staticmethod
    def get_by_id(db: Session, orden_id: int):
        return db.query(OrdenVenta).filter(OrdenVenta.id == orden_id).first()

    @staticmethod
    def create(db: Session, orden: OrdenVentaCreate):
        db_orden = OrdenVenta(**orden.model_dump())
        db.add(db_orden)
        db.commit()
        db.refresh(db_orden)
        return db_orden

    @staticmethod
    def update(db: Session, orden_id: int, orden: OrdenVentaUpdate):
        db_orden = OrdenVentaRepository.get_by_id(db, orden_id)

        if not db_orden:
            return None

        for key, value in orden.model_dump(exclude_unset=True).items():
            setattr(db_orden, key, value)

        db.commit()
        db.refresh(db_orden)
        return db_orden

    @staticmethod
    def delete(db: Session, orden_id: int):
        db_orden = OrdenVentaRepository.get_by_id(db, orden_id)

        if not db_orden:
            return None

        db.delete(db_orden)
        db.commit()
        return db_orden
