from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.models.receta_model import Receta
from app.models.transaccion_model import Transaccion
from app.models.cliente_model import Cliente
from datetime import datetime, timezone, timedelta

class PanelRepository:

    @staticmethod
    def get_today(db: Session, target_date: date = None):
        if target_date is None:
            target_date = datetime.now(timezone.utc).date()

        start = datetime.combine(target_date, datetime.min.time())
        end = start + timedelta(days=1)

        count_recetas = db.query(func.count()).filter(
            Receta.fecha_consulta >= start,
            Receta.fecha_consulta < end
        ).scalar()

        sum_transacciones = db.query(func.sum(Transaccion.monto_abonado)).filter(
            Transaccion.fecha_pago >= start,
            Transaccion.fecha_pago < end
        ).scalar() or 0.0

        clientes = db.query(
            Cliente.id,
            Cliente.nombre_completo,
            Cliente.fecha_registro
        ).filter(
            Cliente.fecha_registro >= start,
            Cliente.fecha_registro < end
        ).all()

        return {
            "fecha": target_date,
            "pacientes_atendidos": count_recetas,
            "venta_del_dia": sum_transacciones,
            "clientes": clientes
        }