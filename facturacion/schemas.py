from pydantic import BaseModel
from typing import Optional
from datetime import date

class FacturacionBase(BaseModel):
    tarjeta_emisor_id: Optional[int]
    nro_tarjeta: Optional[int]
    vto_fecha: Optional[date]
    cod_verificacion: Optional[int]

class Facturacion(FacturacionBase):
    fecha_alta: date
    fecha_baja: date
    id: int
    activo: bool

    class Config:
        orm_mode = True