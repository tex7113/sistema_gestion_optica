from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import UsuarioService
from app.dependencies.auth_dependency import require_role

router = APIRouter()

@router.get("/", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=list[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    return UsuarioService.listar_usuarios(db)

@router.get("/{usuario_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=UsuarioResponse)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService.obtener_por_id(db, usuario_id)

@router.post("/", response_model=UsuarioResponse, dependencies=[Depends(require_role(["ADMIN"]))])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService.crear_usuario(db, usuario)

@router.put("/{usuario_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=UsuarioResponse)
def actualizar_usuarios(usuario_id:int, usuario:UsuarioCreate, db:Session = Depends(get_db)):
    return UsuarioService.actualizar(db, usuario_id, usuario)


@router.put("/desactivar-usuario/{usuario_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=UsuarioResponse)
def desactivar_usuarios(usuario_id: int, db:Session = Depends(get_db)):
    return UsuarioService.eliminar(db, usuario_id)

@router.put("/activar-usuario/{usuario_id}", dependencies=[Depends(require_role(["ADMIN", "VENDEDOR"]))], response_model=UsuarioResponse)
def activar_usuarios(usuario_id: int, db:Session = Depends(get_db)):
    return UsuarioService.activar(db, usuario_id)