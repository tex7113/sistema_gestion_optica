from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import UsuarioService
from app.dependencies.auth_dependency import require_role

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, dependencies=[Depends(require_role(["ADMIN"]))])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService.crear_usuario(db, usuario)