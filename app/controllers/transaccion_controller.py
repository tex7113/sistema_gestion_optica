from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.transaccion_schema import TransaccionCreate, PagoResponse
from app.services.transaccion_service import TransaccionService
from fastapi.responses import Response
from app.dependencies.auth_dependency import require_role, get_current_user

router = APIRouter()

@router.post("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PagoResponse)
def crear(transaccion: TransaccionCreate, usuario = Depends(get_current_user),db: Session = Depends(get_db)):
    return TransaccionService.crear(db, transaccion, usuario.id)

@router.get("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))])
def saldo_pendiente(orden_venta_id: int, db: Session = Depends(get_db)):
    return TransaccionService.saldo_pendiente(db, orden_venta_id)

@router.get("/ticket/{id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))])
def descargar_ticket(transaccion_id: int, db: Session = Depends(get_db)):
    pdf = TransaccionService.generar_ticket_pago(db, transaccion_id)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f"attachment; filename=ticket_{transaccion_id}.pdf"
        }
    )