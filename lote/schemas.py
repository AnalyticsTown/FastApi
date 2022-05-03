from typing import Optional

from pydantic import BaseModel, Field

class LoteBase(BaseModel):
    codigo: str
    poligono: Optional[str]
    superficie: Optional[float]
    superficie_calculada: Optional[float] # Se agrego este campo
    establecimiento_id: Optional[int] = Field(default=None, foreign_key="establecimientos.id") # Se movió de lote a acá

class Lote(LoteBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True