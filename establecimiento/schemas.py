from pydantic import BaseModel, validator, ValidationError
from fastapi.exceptions import HTTPException
from typing import Optional
from datetime import date, datetime

class EstablecimientoBase(BaseModel):
    nombre: str
    abreviatura: str
    establecimiento_tipo_id: Optional[str]
    direccion: Optional[str]
    localidad: Optional[str]
    provincia: Optional[str]
    pais: Optional[str]
    latitud: Optional[str]
    longitud: Optional[str]
    zona_id: Optional[str]
    observaciones: Optional[str]

class Establecimiento(EstablecimientoBase):
    id: int
    ser_id: Optional[int]
    created: datetime
    modified: datetime
    deleted: Optional[datetime]

    class Config:
        orm_mode = True