from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import FetchedValue


class InsumoValuacion(BaseModel):
    
    cantidad: int
    precio_unitario: float
    almacen_id: int
    movimiento: str
    tipo_movimiento_id: str
    insumo_id: str


class Metodo_valorizacion_empresa(BaseModel):
    empresa_id: int
    metodo_id: int
