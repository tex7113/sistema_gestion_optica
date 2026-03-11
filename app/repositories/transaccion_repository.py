from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.transaccion_model import Transaccion


class TransaccionRepository:

    @staticmethod
    def get_by_id(db: Session, transaccion_id: int):
        return db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()

    @staticmethod
    def create(db: Session, transaccion, usuario_id: int):
        trans = Transaccion(**transaccion.model_dump(), usuario_id = usuario_id)
        db.add(trans)
        db.commit()
        db.refresh(trans)
        return trans

    @staticmethod
    def total_paid(db: Session, orden_id: int, date: datetime = None):
        query = db.query(func.coalesce(func.sum(Transaccion.monto_abonado), 0)).filter(
            Transaccion.orden_venta_id == orden_id
        )
        if date:
            query = query.filter(Transaccion.fecha_pago <= date)
        return query.scalar()

    @staticmethod
    def total_payments(db: Session, orden_id, date: datetime = None):
        query = db.query(func.count(Transaccion.id)).filter(Transaccion.orden_venta_id == orden_id)
        if date:
            query = query.filter(Transaccion.fecha_pago <= date)
        return query.scalar()

    @staticmethod
    def history_by_orden_id(db: Session, orden_id, date: datetime = None):
        query = db.query(Transaccion).filter(Transaccion.orden_venta_id == orden_id)
        if datetime:
            query = query.filter(Transaccion.fecha_pago <= date)
        return query.all()