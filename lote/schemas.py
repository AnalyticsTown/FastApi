from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoteBase(BaseModel):
    codigo: str
    establecimiento_id: Optional[int]
    superficie: float
    poligono: float

class Lote(LoteBase):
    id: int
    usuario_id: Optional[int]
    created: datetime
    modified: datetime
    deleted: Optional[datetime]

    class Config:
        orm_mode = True