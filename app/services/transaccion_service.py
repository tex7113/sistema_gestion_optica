from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.orden_venta_repository import OrdenVentaRepository
from app.schemas.orden_venta_schema import OrdenVentaResponse


class TransaccionService:

    @staticmethod
    def crear(db: Session, transaccion):

        db_orden = OrdenVentaRepository.get_by_id(db, transaccion.orden_venta_id)

        if not db_orden:
            raise HTTPException(404, "La orden de venta no existe")

        if db_orden.tipo_pago == "CONTADO" or db_orden.estado_pago == "PAGADO":
            raise HTTPException(status_code=404, detail="No se puede crear una transaccion para la orden de venta seleccionada")

        total_abonado = TransaccionRepository.total_paid(db, transaccion.orden_venta_id)

        nuevo_total = total_abonado + transaccion.monto_abonado

        if nuevo_total > db_orden.monto_total:
            raise HTTPException(400,"El abono excede el monto total")

        db_transaccion = TransaccionRepository.create(db, transaccion)

        # Actualizar estado automáticamente
        if nuevo_total == db_orden.monto_total:
            db_orden.estado_pago = "PAGADO"
            db.commit()

        return db_transaccion


    @staticmethod
    def saldo_pendiente(db: Session, orden_venta_id: int):
        db_orden_venta: OrdenVentaResponse = OrdenVentaRepository.get_by_id(db, orden_venta_id)
        total_abonado = TransaccionRepository.total_paid(db, orden_venta_id)
        return str(db_orden_venta.monto_total - total_abonado)