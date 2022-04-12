from pydantic import BaseModel
from typing import Optional

class LoteBase(BaseModel):
    codigo: str
    superficie: Optional[float]
    poligono: Optional[str]

class Lote(LoteBase):
    id: int
    activo: bool
    establecimiento_id: Optional[int]

    class Config:
        orm_mode = True