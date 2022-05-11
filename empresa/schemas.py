from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class CondicionIva(BaseModel):
    id: int
    detalle_cond_iva: str

    class Config:
        orm_mode = True

class Moneda(BaseModel):
    id: int
    detalle_moneda: str

    class Config:
        orm_mode = True

class RubroEmpresa(BaseModel):
    id: int
    detalle_rubro_empresa: str

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
    cond_iva_id: Optional[int] = Field(default=None, foreign_key="cond_ivas.id")
    moneda_primaria_id: Optional[int] = Field(default=None, foreign_key="monedas.id")
    moneda_secundaria_id: Optional[int] = Field(default=None, foreign_key="monedas.id")
    rubro_empresa_id: Optional[int] = Field(default=None, foreign_key="rubro_empresas.id")

class Empresa(EmpresaBase):
    id: int
    activo: bool
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario_empresas.usuario_id")
    #usuario_admin: Optional[str] = Field(default=None, foreign_key="admins.id_token")
    class Config:
        orm_mode = True