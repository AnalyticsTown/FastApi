from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class TipoErogacion(BaseModel):
    id: int
    nombre: str
    abreviatura: str

    class Config:
        orm_mode = True

class Unidad(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class Tarea(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class Familia(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class Subfamilia(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class RubroInsumo(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class InsumoBase(BaseModel):
    nombre: str
    abreviatura: str
    codigo_externo: Optional[str]
    lote_control: Optional[bool]
    vencimiento_control: Optional[bool]
    reposicion_control: Optional[bool]
    reposicion_cantidad: Optional[int]
    reposicion_alerta: Optional[bool]
    reposicion_alerta_email: Optional[EmailStr]
    tarea_id: Optional[int]
    unidad_id: Optional[int]
    familia_id: Optional[int]
    subfamilia_id: Optional[int]
    rubro_insumo_id: Optional[int]
    tipo_erogacion_id: Optional[int]

class Insumo(InsumoBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True