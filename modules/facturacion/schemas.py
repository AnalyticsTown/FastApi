from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class FacturacionBase(BaseModel):
    tarjeta_emisor_id: Optional[int] = Field(default=None, foreign_key="emisor_tarjetas.id")
    nro_tarjeta: Optional[int]
    vto_fecha: Optional[date]
    cod_verificacion: Optional[int]

class Facturacion(FacturacionBase):
    id: int
    activo: bool
    fecha_alta: date
    fecha_baja: date

    class Config:
        orm_mode = True