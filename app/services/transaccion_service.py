from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.orden_venta_repository import OrdenVentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.schemas.orden_venta_schema import OrdenVentaResponse
from app.schemas.orden_venta_schema import OrdenVentaResumen
from app.schemas.transaccion_schema import TransaccionResponse, TransaccionCreate
from app.services.orden_venta_service import OrdenVentaService
from app.utils.pdf_generator import generar_ticket


class TransaccionService:


    @staticmethod
    def obtener_por_id(db: Session, transaccion_id: int):
        db_transaccion = TransaccionRepository.get_by_id(db, transaccion_id)
        if db_transaccion is None:
            raise HTTPException(status_code=404, detail=f"No se encontro ninguna transaccion con id: {transaccion_id}")
        return db_transaccion

    @staticmethod
    def listar(db:Session):
        return TransaccionRepository.get_all(db)

    @staticmethod
    def crear(db: Session, transaccion: TransaccionCreate, usuario_id: int):

        try:

            total_abonado = 0

            db_orden: OrdenVentaResponse = OrdenVentaRepository.get_by_id(db, transaccion.orden_venta_id)

            if not db_orden:
                raise HTTPException(404, "La orden de venta no existe")

            if db_orden.estado_pago == "PAGADO":
                raise HTTPException(status_code=400, detail="La orden de venta seleccionada ya hacido pagada")

            if db_orden.tipo_pago == "CONTADO" and db_orden.monto_total > transaccion.monto_abonado:
                raise HTTPException(status_code=400, detail="El monto abonado es insuficiente para pagar el monto total")

            if db_orden.tipo_pago == "CREDITO":
                total_abonado = TransaccionRepository.total_paid(db, transaccion.orden_venta_id)

            nuevo_total = total_abonado + transaccion.monto_abonado

            if nuevo_total > db_orden.monto_total:
                raise HTTPException(400,"El monto abonado excede el monto total")

            db_transaccion = TransaccionRepository.create(db, transaccion, usuario_id)

            # Actualizar estado automáticamente
            if nuevo_total == db_orden.monto_total:
                db_orden.estado_pago = "PAGADO"

            db.commit()
            db.refresh(db_orden)
            resumen_pago = OrdenVentaService.resumen_financiero(db, transaccion.orden_venta_id)

            return {
                "transaccion": db_transaccion,
                "resumen_pago": resumen_pago
            }
        except Exception as e:
            db.rollback()
            raise


    @staticmethod
    def saldo_pendiente(db: Session, orden_venta_id: int):
        db_orden_venta: OrdenVentaResponse = OrdenVentaRepository.get_by_id(db, orden_venta_id)
        total_abonado = TransaccionRepository.total_paid(db, orden_venta_id)
        return str(db_orden_venta.monto_total - total_abonado)


    @staticmethod
    def generar_ticket_pago(db: Session, transaccion_id: int):
        db_transaccion: TransaccionResponse = TransaccionRepository.get_by_id(db, transaccion_id)
        if db_transaccion is None:
            raise HTTPException(status_code=404, detail="No se encontro ninguna transaccion")

        db_resumen:OrdenVentaResumen = OrdenVentaService.resumen_financiero(db, db_transaccion.orden_venta_id, db_transaccion.fecha_pago)
        if db_resumen is None:
            raise HTTPException(status_code=404, detail="error")

        data = {
            "orden_id": db_transaccion.orden_venta_id,
            "transaccion_id": db_transaccion.id,
            "cliente_nombre": db_resumen.cliente_nombre,
            "cliente_telefono": db_resumen.cliente_telefono,
            "fecha": db_transaccion.fecha_pago,
            "metodo_pago": db_transaccion.metodo_pago,
            "monto": db_transaccion.monto_abonado,
            "total": db_resumen.monto_total,
            "pagado": db_resumen.total_abonado,
            "restante": db_resumen.saldo_pendiente
        }

        return generar_ticket(data)