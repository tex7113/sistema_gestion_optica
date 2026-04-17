from fastapi import APIRouter, Depends
from sqlalchemy.orm import  Session
from app.core.database import get_db
from app.schemas.plan_pago_schemas import PlanPagoCreate, PlanPagoResponse
from app.services.plan_pago_service import PlanPagoService
from app.dependencies.auth_dependency import require_role

router = APIRouter()

@router.get("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=list[PlanPagoResponse])
def obtener_planes_de_pagos(db: Session = Depends(get_db)):
    return PlanPagoService.listar(db)

@router.get("/{plan_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PlanPagoResponse)
def obtener_plan_de_pago_por_id(plan_id: int, db: Session = Depends(get_db)):
    return PlanPagoService.obtener_por_id(db, plan_id)

@router.post("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PlanPagoResponse)
def crear(plan_pago: PlanPagoCreate, db: Session = Depends(get_db)):
    return PlanPagoService.crear(db, plan_pago)

@router.put("/{plan_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PlanPagoResponse)
def actualizar_plan_de_pagos(plan_id:int, plan:PlanPagoCreate, db:Session = Depends(get_db)):
    return PlanPagoService.actualizar(db, plan_id, plan)

@router.delete("/{plan_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=PlanPagoResponse)
def eliminar_plan_de_pagos(plan_id: int, db:Session = Depends(get_db)):
    return PlanPagoService.eliminar(db, plan_id)