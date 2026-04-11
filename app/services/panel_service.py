from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.panel_repository import PanelRepository


class PanelService:

    @staticmethod
    def obtener_informacion_del_dia(db: Session, fecha: datetime = None):
        return PanelRepository.get_today(db, fecha)
