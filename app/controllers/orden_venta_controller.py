from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.orden_venta_schema import OrdenVentaCreate, OrdenVentaUpdate, OrdenVentaResponse, OrdenVentaSumary
from app.services.orden_venta_service import OrdenVentaService
from app.dependencies.auth_dependency import require_role

router = APIRouter()


@router.get("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=list[OrdenVentaResponse])
def listar_ordenes_de_ventas(db: Session = Depends(get_db)):
    return OrdenVentaService.listar(db)


@router.get("/{orden_id}", response_model=OrdenVentaResponse)
def obtener_orden_de_venta(orden_id: int, db: Session = Depends(get_db)):
    return OrdenVentaService.obtener_por_id(db, orden_id)


@router.post("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=OrdenVentaResponse)
def crear_orden_de_venta(orden: OrdenVentaCreate, db: Session = Depends(get_db)):
    return OrdenVentaService.crear(db, orden)


@router.put("/{orden_id}", response_model=OrdenVentaResponse)
def actualizar_orden_de_venta(orden_id: int,orden: OrdenVentaUpdate,db: Session = Depends(get_db)):
    return OrdenVentaService.actualizar(db, orden_id, orden)


@router.delete("/{orden_id}",response_model=OrdenVentaResponse)
def eliminar_orden_de_venta(orden_id: int,db: Session = Depends(get_db)):
    return OrdenVentaService.eliminar(db, orden_id)

@router.get("/{orden_id}/resumen", response_model=OrdenVentaSumary)
def resumen_financiero(orden_id:int, db: Session = Depends(get_db)):
    return OrdenVentaService.resumen_financiero(db, orden_id)