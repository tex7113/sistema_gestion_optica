from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.plan_pago_repository import PlanPagoRepository
from app.repositories.orden_venta_repository import OrdenVentaRepository
from app.schemas.plan_pago_schemas import (PlanPagoCreate)


class PlanPagoService:

    @staticmethod
    def listar(db: Session):
        return PlanPagoRepository.get_all(db)

    @staticmethod
    def obtener_por_id(db:Session, plan_id):
        return PlanPagoRepository.get_by_id(db, plan_id)

    @staticmethod
    def crear(db: Session, data):

        db_orden = OrdenVentaRepository.get_by_id(db, data.orden_venta_id)

        if not db_orden:
            raise HTTPException(404, "La orden de venta no existe")

        if db_orden.estado_pago == "PAGADO":
            raise HTTPException(400,"La orden de venta seleccionada ya hacido pagada")

        if db_orden.tipo_pago != "CREDITO":
            raise HTTPException(400,"Solo órdenes de venta a crédito pueden tener plan de pagos")

        if PlanPagoRepository.get_by_orden_venta(db, data.orden_venta_id):
            raise HTTPException(400,"La orden de venta ya tiene un plan de pago")

        return PlanPagoRepository.create(db, data)

    @staticmethod
    def actualizar(db: Session, plan_id: int, plan: PlanPagoCreate):
        db_plan = PlanPagoRepository.update(db, plan_id, plan)
        if db_plan is None:
            raise HTTPException(status_code=404, detail=f"El plan de pagos con la id:{plan_id} no encontrado")
        return db_plan

    @staticmethod
    def eliminar(db:Session, plan_id: int):
        db_plan = PlanPagoRepository.delet(db, plan_id)
        if db_plan is None:
            raise HTTPException(status_code=404, detail=f"El plan de pagos con la id:{plan_id} no encontrado")
        return db_plan