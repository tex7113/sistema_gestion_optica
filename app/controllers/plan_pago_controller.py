from fastapi import APIRouter, Depends
from sqlalchemy.orm import  Session
from app.core.database import get_db
from app.schemas.plan_pago_schemas import PlanPagoCreate, PlanPagoResponse
from app.services.plan_pago_service import PlanPagoService

router = APIRouter()

@router.post("/", response_model=PlanPagoResponse)
def crear(plan_pago: PlanPagoCreate, db: Session = Depends(get_db)):
    return PlanPagoService.crear(db, plan_pago)