from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.plan_pago_repository import PlanPagoRepository
from app.repositories.orden_venta_repository import OrdenVentaRepository


class PlanPagoService:

    @staticmethod
    def listar(db: Session):
        return PlanPagoRepository.get_all(db)

    @staticmethod
    def crear(db: Session, data):

        db_orden = OrdenVentaRepository.get_by_id(db, data.orden_venta_id)

        if not db_orden:
            raise HTTPException(404, "La orden de venta no existe")

        if db_orden.tipo_pago != "CREDITO":
            raise HTTPException(400,"Solo órdenes de venta a crédito pueden tener plan de pagos")

        if PlanPagoRepository.get_by_orden_venta(db, data.orden_venta_id):
            raise HTTPException(400,"La orden de venta ya tiene un plan de pago")

        return PlanPagoRepository.create(db, data)