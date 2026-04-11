from pydantic import BaseModel
from datetime import date

class PanelResponse(BaseModel):
    fecha: date
    pacientes_atendidos: int
    venta_del_dia: str