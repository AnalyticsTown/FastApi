from pydantic import BaseModel
from typing import Optional
from datetime import date

class FacturacionBase(BaseModel):
    tarjeta_emisor_id: Optional[int]
    nro_tarjeta: int
    vto_fecha: date
    cod_verificacion: int
    fecha_alta: date
    fecha_baja: date

class Facturacion(FacturacionBase):
    id: int

    class Config:
        orm_mode = True