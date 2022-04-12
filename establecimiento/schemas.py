from pydantic import BaseModel
from typing import Optional

class TipoEstablecimiento(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class Zona(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class EstablecimientoBase(BaseModel):
    nombre: str
    abreviatura: str
    direccion: Optional[str]
    localidad: Optional[str]
    provincia: Optional[str]
    pais: Optional[str]
    latitud: Optional[str]
    longitud: Optional[str]
    observaciones: Optional[str]
    contacto: Optional[str]
    zona_id: Optional[int]
    establecimiento_tipo_id: Optional[int]

class Establecimiento(EstablecimientoBase):
    id: int
    activo: bool
    empresa_id: Optional[int]

    class Config:
        orm_mode = True