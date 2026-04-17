from typing import List
from datetime import datetime
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class PanelResponse(BaseModel):
    fecha: date
    pacientes_atendidos: int
    venta_del_dia: Decimal
    clientes: List[ClientePanelResponse] = []

class ClientePanelResponse(BaseModel):
    id: int
    nombre_completo: str
    fecha_registro: datetime