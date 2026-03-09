from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.orden_venta_repository import OrdenVentaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.receta_repository import RecetaRepository
from app.schemas.orden_venta_schema import OrdenVentaCreate, OrdenVentaUpdate, OrdenVentaResponse, OrdenVentaResumen
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.plan_pago_repository import PlanPagoRepository
from app.schemas.plan_pago_schemas import PlanPagoResponse
from app.schemas.cliente_schema import ClienteResponse

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

    @staticmethod
    def resumen_financiero(db: Session, orden_id: int, fecha_hasta: datetime = None):

        db_orden:OrdenVentaResponse = OrdenVentaRepository.get_by_id(db, orden_id)

        if not db_orden:
            raise HTTPException(404, "Orden no encontrada")

        db_cliente:ClienteResponse = ClienteRepository.get_cliente_by_id(db, db_orden.cliente_id)
        total_abonado = TransaccionRepository.total_paid(db, orden_id, fecha_hasta)
        cantidad_pagos = TransaccionRepository.total_payments(db, orden_id, fecha_hasta)

        saldo_pendiente = db_orden.monto_total - total_abonado
        db_plan: PlanPagoResponse = PlanPagoRepository.get_by_orden_venta(db, orden_id)
        pagos_pendientes = None

        if db_plan:
            pagos_pendientes = db_plan.numero_plazos - cantidad_pagos
            if pagos_pendientes < 0:
                pagos_pendientes = 0

        return OrdenVentaResumen(
            orden_id=db_orden.id,
            cliente=db_cliente.nombre_completo,
            monto_total=db_orden.monto_total,
            total_abonado=total_abonado,
            saldo_pendiente=saldo_pendiente,
            pagos_realizados=cantidad_pagos,
            pagos_pendientes=pagos_pendientes,
            estado_pago=db_orden.estado_pago,
        )

    @staticmethod
    def historial_transacciones(db: Session, orden_id: int):
        db_orden: OrdenVentaResponse = OrdenVentaRepository.get_by_id(db, orden_id)

        if not db_orden:
            raise HTTPException(404, "Orden de venta no encontrada")

        db_transacciones = TransaccionRepository.history_by_orden_id(db, orden_id)

        return db_transacciones