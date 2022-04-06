from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class InsumoBase(BaseModel):

    nombre: str
    abreviatura: str
    codigo_externo: str
    lote_control: bool
    lote_numero: str
    vencimiento_control: bool
    vencimiento_fecha: date
    reposicion_control: bool
    reposicion_cantidad: int
    reposicion_alerta: str
    tipo_erogacione_id: Optional[int]
    unidade_id: Optional[int]
    rubro_insumo_id: Optional[int]
    familia_id: Optional[int]
    subfamilia_id: Optional[int]

class Insumo(InsumoBase):
    id: int
    usuario_id: Optional[int]
    created: datetime
    modified: datetime
    deleted: Optional[datetime]

    class Config:
        orm_mode = True