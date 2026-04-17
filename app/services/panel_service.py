from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.panel_repository import PanelRepository


class PanelService:

    @staticmethod
    def obtener_informacion_del_dia(db: Session, fecha = None):
        if fecha is not None:
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="valores incorrectos. Asegurese de mandar formato: YYYY-MM-DD")

        return PanelRepository.get_today(db, fecha)
