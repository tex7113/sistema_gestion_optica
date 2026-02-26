from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaccion_model import Transaccion


class TransaccionRepository:

    @staticmethod
    def create(db: Session, transaccion):
        trans = Transaccion(**transaccion.model_dump())
        db.add(trans)
        db.commit()
        db.refresh(trans)
        return trans

    @staticmethod
    def total_paid(db: Session, orden_id: int):
        total = db.query(func.coalesce(func.sum(Transaccion.monto_abonado), 0)).filter(Transaccion.orden_venta_id == orden_id).scalar()
        return total

    @staticmethod
    def total_payments(db: Session, orden_id):
        return  db.query(func.count(Transaccion.id)).filter(Transaccion.orden_venta_id == orden_id).scalar()

    @staticmethod
    def history_by_orden_id(db: Session, orden_id):
        return db.query(Transaccion).filter(Transaccion.orden_venta_id == orden_id).all()