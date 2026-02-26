from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionResponse
from app.services.transaccion_service import TransaccionService

router = APIRouter()

@router.post("/", response_model=TransaccionResponse)
def crear(transaccion: TransaccionCreate,db: Session = Depends(get_db)):
    return TransaccionService.crear(db, transaccion)

@router.get("/")
def saldo_pendiente(orden_venta_id: int, db: Session = Depends(get_db)):
    return TransaccionService.saldo_pendiente(db, orden_venta_id)