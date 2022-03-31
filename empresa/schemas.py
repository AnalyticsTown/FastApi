from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmpresaBase(BaseModel):
    razon_social: str
    direccion_calle: str
    direccion_nro: str
    direccion_localidad: str
    direccion_provincia: str
    direccion_pais: str
    direccion_cod_postal: str
    cuit: Optional[int] | None = None
    cond_iva_id: Optional[str] | None = None
    fecha_cierre: date
    moneda_primaria_id: Optional[str]
    moneda_secundaria_id: Optional[str]

class Empresa(EmpresaBase):
    id: int
    rubro_id: Optional[int]

    class Config:
        orm_mode = True