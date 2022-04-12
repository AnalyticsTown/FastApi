from pydantic import BaseModel
from typing import Optional

class TipoAlmacen(BaseModel):
    id: int
    detalle: Optional[str]

    class Config:
        orm_mode = True

class AlmacenBase(BaseModel):
    nombre: str
    abreviatura: str
    descripcion: Optional[str]
    geoposicion: Optional[str]
    observaciones: Optional[str]
    almacenes_tipo_id: Optional[int]

class Almacen(AlmacenBase):
    id: int
    activo: bool
    establecimiento_id: Optional[int]

    class Config:
        orm_mode = True