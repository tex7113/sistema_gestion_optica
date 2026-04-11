from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.panel_service import PanelService
from datetime import datetime
from app.dependencies.auth_dependency import require_role
from app.schemas.panel_schema import PanelResponse

router = APIRouter()

@router.get("/",response_model=PanelResponse, dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))])
def panel_principal(
        fecha: str = Query(None, description="Fecha a consultar, ej. YYYY-MM-DD. Automatico Hoy"),
        db: Session = Depends(get_db)
):
    if fecha:
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

    return PanelService.obtener_informacion_del_dia(db,fecha)