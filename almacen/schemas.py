from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlmacenBase(BaseModel):
    nombre: str
    abreviatura: str
    descripcion: str
    establecimiento_id: Optional[int]
    almacenes_tipo_id: Optional[int]
    geoposicion: str
    observaciones: str

class Almacen(AlmacenBase):
    id: int
    usuario_id: Optional[int]
    created: datetime
    modified: datetime
    deleted: Optional[datetime]

    class Config:
        orm_mode = True