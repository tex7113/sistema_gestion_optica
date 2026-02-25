from fastapi import FastAPI
from app.core.config import settings
from app.controllers import cliente_controller
from app.controllers import receta_controller
from app.controllers import orden_venta_controller

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(cliente_controller.router, prefix='/clientes', tags=['CLIENTES (clientes)'])
app.include_router(receta_controller.router, prefix="/recetas", tags=["RECETAS (recetas)"])
app.include_router(orden_venta_controller.router, prefix="/orden-venta", tags=["ORDENES DE VENTA (ordenes de venta)"])

@app.get("/")
def root():
    return {"message": "Sistema de Gestion Optica"}