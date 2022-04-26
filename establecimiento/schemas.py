from typing import Optional

from pydantic import BaseModel, Field

class Zona(BaseModel):
    id: int
    detalle_zona: str

    class Config:
        orm_mode = True

class TipoEstablecimiento(BaseModel):
    id: int
    detalle_tipo_establecimiento: str

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
    zona_id: Optional[int] = Field(default=None, foreign_key="zonas.id")
    establecimiento_tipo_id: Optional[int] = Field(default=None, foreign_key="tipo_establecimientos.id")

class Establecimiento(EstablecimientoBase):
    id: int
    activo: bool
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresas.id")
    almacen_id: Optional[int] = Field(default=None, foreign_key="establecimiento_almacenes.almacen_id")

    class Config:
        orm_mode = True