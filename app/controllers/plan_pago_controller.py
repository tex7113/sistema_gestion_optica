from fastapi import APIRouter, Depends
from sqlalchemy.orm import  Session
from app.core.database import get_db
from app.schemas.plan_pago_schemas import PlanPagoCreate, PlanPagoResponse
from app.services.plan_pago_service import PlanPagoService
from app.dependencies.auth_dependency import require_role

router = APIRouter()

@router.get("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=list[PlanPagoResponse])
def obtener_planes_pagos(db: Session = Depends(get_db)):
    return PlanPagoService.listar(db)

@router.post("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PlanPagoResponse)
def crear(plan_pago: PlanPagoCreate, db: Session = Depends(get_db)):
    return PlanPagoService.crear(db, plan_pago)