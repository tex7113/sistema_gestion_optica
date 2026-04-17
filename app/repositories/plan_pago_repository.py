from sqlalchemy.orm import Session
from app.models.plan_pago_model import PlanPago
from app.schemas.plan_pago_schemas import PlanPagoCreate


class PlanPagoRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(PlanPago).all()

    @staticmethod
    def get_by_id(db:Session, plan_id: int):
        return db.query(PlanPago).filter(PlanPago.id == plan_id).first()

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

    @staticmethod
    def update(db:Session, plan_id: int, plan: PlanPagoCreate):
        db_plan = PlanPagoRepository.get_by_id(db, plan_id)

        if not db_plan:
            return None
        for key, value in plan.model_dump(exclude_unset=True).items():
            setattr(db_plan, key, value)
        db.commit()
        db.refresh(db_plan)
        return db_plan

    @staticmethod
    def delet(db:Session, plan_id):
        db_plan = PlanPagoRepository.get_by_id(db, plan_id)

        if not db_plan:
            return None
        db.delete(db_plan)
        db.commit()
        return db_plan