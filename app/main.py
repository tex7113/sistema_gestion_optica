from fastapi import FastAPI
from app.core.config import settings
from app.controllers import cliente_controller
from app.controllers import receta_controller
from app.controllers import orden_venta_controller
from app.controllers import plan_pago_controller
from app.controllers import transaccion_controller
from app.controllers import auth_controller
from app.controllers import usuario_controller

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(cliente_controller.router, prefix='/clientes', tags=['CLIENTES (clientes)'])
app.include_router(receta_controller.router, prefix="/recetas", tags=["RECETAS (recetas)"])
app.include_router(orden_venta_controller.router, prefix="/ordenes-de-venta", tags=["ORDENES DE VENTA (ordenes de venta)"])
app.include_router(plan_pago_controller.router, prefix="/planes-de-pago", tags=["PLANES DE PAGO (planes de pago)"])
app.include_router(transaccion_controller.router, prefix="/transacciones", tags=["TRANSACCIONES (transacciones)"])
app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
app.include_router(usuario_controller.router, prefix="/usuario", tags=["Usuarios"])

@app.get("/")
def root():
    return {"message": "Sistema de Gestion Optica"}