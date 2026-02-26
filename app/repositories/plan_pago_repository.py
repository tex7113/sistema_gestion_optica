from sqlalchemy.orm import Session
from app.models.plan_pago_model import PlanPago


class PlanPagoRepository:

    @staticmethod
    def get_by_orden_venta(db: Session, orden_venta_id: int):
        return db.query(PlanPago).filter(PlanPago.orden_venta_id == orden_venta_id).first()

    @staticmethod
    def create(db: Session, data):
        db_plan = PlanPago(**data.model_dump())
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan