from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.models.receta_model import Receta
from app.models.transaccion_model import Transaccion

class PanelRepository:

    @staticmethod
    def get_today(db: Session, target_date: date = None):
        if target_date is None:
            target_date = datetime.utcnow().date()

        # Contar recetas por fecha_consulta
        count_recetas = db.query(func.count()).filter(
            func.date(Receta.fecha_consulta) == target_date
        ).scalar()

        # Sumar monto_abonado por fecha_pago
        sum_transacciones = db.query(func.sum(Transaccion.monto_abonado)).filter(
            func.date(Transaccion.fecha_pago) == target_date
        ).scalar() or 0.0

        return {
            "fecha": target_date,
            "pacientes_atendidos": count_recetas,
            "venta_del_dia": str(sum_transacciones)
        }