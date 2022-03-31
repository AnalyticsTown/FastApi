from pydantic import BaseModel, validator, ValidationError
from fastapi.exceptions import HTTPException
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
    cond_iva_id: Optional[str]
    fecha_cierre: date
    moneda_primaria_id: Optional[str]
    moneda_secundaria_id: Optional[str]

    # @validator('cuit')
    # def cuit_if_argentina(cls, v, values, **kwargs):
    #     if (values['direccion_pais'] == 'Argentina' and v == None):
    #         raise HTTPException(status_code=400, detail="Completar CUIT")
    #     return v

class Empresa(EmpresaBase):
    id: int
    rubro_id: Optional[int]

    class Config:
        orm_mode = True