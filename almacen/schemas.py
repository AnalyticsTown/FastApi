from typing import Optional
from pydantic import BaseModel, Field

class TipoAlmacen(BaseModel):
    id: int
    detalle_tipo_almacen: Optional[str]

    class Config:
        orm_mode = True

class AlmacenBase(BaseModel):
    nombre: str
    abreviatura: str
    descripcion: Optional[str]
    geoposicion: Optional[str]
    observaciones: Optional[str]
    almacenes_tipo_id: Optional[int] = Field(default=None, foreign_key="tipo_almacenes.id")
    #establecimiento_id: Optional[int] #= Field(default=None, foreign_key="establecimiento_almacenes.establecimiento_id")
    
    class Config:
        orm_mode = True

class Almacen(AlmacenBase):
    id: int
    activo: bool
    
    class Config:
        orm_mode = True