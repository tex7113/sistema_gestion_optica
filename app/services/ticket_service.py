from app.utils.pdf_generator import generar_ticket

class TicketService:

    @staticmethod
    def generar_ticket_pago(transaccion, resumen):

        data = {
            "orden_id": transaccion.orden_venta_id,
            "transaccion_id": transaccion.id,
            "cliente": transaccion.orden.cliente.nombre,
            "fecha": transaccion.fecha_pago,
            "metodo_pago": transaccion.metodo_pago,
            "monto": transaccion.monto_abonado,
            "total": resumen.monto_total,
            "pagado": resumen.total_pagado,
            "restante": resumen.saldo_restante
        }

        return generar_ticket(data)