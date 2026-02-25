from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse, ClienteDetailResponse
from app.services.cliente_service import ClienteService

router = APIRouter()

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar(db)

@router.get("/{cliente_id}", response_model=ClienteDetailResponse)
def obtener_cliente_por_id(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteService.obtener_por_id(db, cliente_id)

@router.get("/correo-electronico/{cliente_correo}", response_model=ClienteDetailResponse)
def obtener_cliente_por_correo_electronico(cliente_correo: str, db: Session = Depends(get_db)):
    return ClienteService.obtener_por_correo(db, cliente_correo)

@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService.crear(db, cliente)

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente:ClienteCreate, db:Session = Depends(get_db)):
    return ClienteService.actualizar(db, cliente_id, cliente)

@router.delete("/{cliente_id}", response_model=ClienteResponse)
def eliminar_cliente(cliente_id: int, db:Session = Depends(get_db)):
    return ClienteService.eliminar(db, cliente_id)