from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Rol(BaseModel):
    id: int
    detalle_rol: str

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: Optional[str]
    apellido: Optional[str]
    dni: Optional[int]
    email: Optional[EmailStr]
    rol_id: Optional[int]

class Usuario(UsuarioBase):
    id: int
    activo: bool
    fecha_alta: date
    fecha_baja: Optional[date]
    empresa_id: Optional[int]

    class Config:
        orm_mode = True