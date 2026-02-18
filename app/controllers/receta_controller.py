from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.receta_schema import RecetaCreate, RecetaResponse, RecetaUpdate
from app.services.receta_service import RecetaService

router = APIRouter()


@router.get("/", response_model=list[RecetaResponse])
def listar_recetas(db: Session = Depends(get_db)):
    return RecetaService.listar(db)


@router.get("/{receta_id}", response_model=RecetaResponse)
def obtener_receta_por_id(receta_id: int, db: Session = Depends(get_db)):
    return RecetaService.obtener(db, receta_id)

@router.get("/cliente/{cliente_id}", response_model=list[RecetaResponse])
def obtener_recetas_por_cliente_id(cliente_id: int, db: Session = Depends(get_db)):
    return RecetaService.obtener_por_cliente_id(db, cliente_id)


@router.post("/", response_model=RecetaResponse)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db)):
    return RecetaService.crear(db, receta)


@router.put("/{receta_id}", response_model=RecetaResponse)
def actualizar_receta(receta_id: int, receta: RecetaUpdate, db: Session = Depends(get_db)):
    return RecetaService.actualizar(db, receta_id, receta)


@router.delete("/{receta_id}", response_model=RecetaResponse)
def eliminar_receta(receta_id: int, db: Session = Depends(get_db)):
    return RecetaService.eliminar(db, receta_id)
