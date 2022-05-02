from typing import Optional

from pydantic import BaseModel, Field

class LoteBase(BaseModel):
    codigo: str
    poligono: Optional[str]
    superficie: Optional[float]
    superficie_calculada: Optional[float]
    establecimiento_id: Optional[int] = Field(default=None, foreign_key="establecimientos.id")

class Lote(LoteBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True