from typing import Optional

from pydantic import BaseModel, Field

class LoteBase(BaseModel):
    codigo: str
    superficie: Optional[float]
    poligono: Optional[str]

class Lote(LoteBase):
    id: int
    activo: bool
    establecimiento_id: Optional[int] = Field(default=None, foreign_key="establecimientos.id")

    class Config:
        orm_mode = True