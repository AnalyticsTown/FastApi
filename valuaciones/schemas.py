from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import FetchedValue


class InsumoValuacion(BaseModel):
    cantidad: int
    valor_unidad: float
    valor_total: float
    movimiento_entrada: Optional[str]
    movimiento_salida: Optional[str]


class Metodo_valorizacion_empresa(BaseModel):
    empresa_id: int
    metodo_id: int
