from pydantic import BaseModel
from typing import Optional
from datetime import date

class CondicionIva(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class Moneda(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class RubroEmpresa(BaseModel):
    id: int
    detalle: str

    class Config:
        orm_mode = True

class EmpresaBase(BaseModel):
    razon_social: str
    direccion_calle: str
    direccion_nro: str
    direccion_localidad: str
    direccion_provincia: str
    direccion_pais: str
    direccion_cod_postal: str
    cuit: Optional[int] | None = None
    fecha_cierre: date
    cond_iva_id: Optional[int] | None = None
    moneda_primaria_id: Optional[int]
    moneda_secundaria_id: Optional[int]
    rubro_empresa_id: Optional[int]

class Empresa(EmpresaBase):
    id: int
    activo: bool
    usuario_id: Optional[int]

    class Config:
        orm_mode = True