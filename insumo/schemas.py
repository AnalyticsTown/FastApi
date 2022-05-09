from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class Tarea(BaseModel):
    id: int
    detalle_tarea: str

    class Config:
        orm_mode = True

class Unidad(BaseModel):
    id: int
    detalle_unidad: str

    class Config:
        orm_mode = True

class Familia(BaseModel):
    id: int
    detalle_familia: str

    class Config:
        orm_mode = True

class Subfamilia(BaseModel):
    id: int
    detalle_subfamilia: str

    class Config:
        orm_mode = True

class RubroInsumo(BaseModel):
    id: int
    detalle_rubro_insumo: str

    class Config:
        orm_mode = True

class TipoErogacion(BaseModel):
    id: int
    nombre_tipo_erogacion: str
    abreviatura_tipo_erogacion: str

    class Config:
        orm_mode = True

class LoteInsumo(BaseModel):
    id: int
    nro_lote: str
    fecha_vencimiento: date
    stock_id: Optional[int] = Field(default=None, foreign_key="stock_almacen_insumos.id")

    class Config:
        orm_mode = True

class TipoMovimientoInsumo(BaseModel):
    id: int
    detalle_tipo_movimiento_insumo: str

    class Config:
        orm_mode = True

class MovimientoInsumoBase(BaseModel):
    cantidad: float
    fecha_movimiento: date
    insumo_id: int = Field(default=None, foreign_key="insumos.id")
    origen_almacen_id: int = Field(default=None, foreign_key="stock_almacen_insumos.id")
    destino_almacen_id: int = Field(default=None, foreign_key="stock_almacen_insumos.id")
    tipo_movimiento_id: int = Field(default=None, foreign_key="tipo_movimiento_insumos.id")

class MovimientoInsumo(MovimientoInsumoBase):
    id: int
    created_at: date

    class Config:
        orm_mode = True

class StockAlmacenInsumoBase(BaseModel):
    detalle: Optional[str]
    cantidad: Optional[float]
    insumo_id: Optional[int] = Field(default=None, foreign_key="insumos.id")
    almacen_id: Optional[int] = Field(default=None, foreign_key="almacenes.id")

class StockAlmacenInsumo(StockAlmacenInsumoBase):
    id: int

    class Config:
        orm_mode = True

class InsumoBase(BaseModel):
    nombre: str
    abreviatura: str
    codigo_externo: Optional[str]
    lote_control: Optional[bool]
    vencimiento_control: Optional[bool]
    reposicion_control: Optional[bool]
    reposicion_cantidad: Optional[float] # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    reposicion_alerta: Optional[bool]
    reposicion_alerta_email: Optional[EmailStr] # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    tarea_id: Optional[int] = Field(default=None, foreign_key="tareas.id")
    unidad_id: Optional[int] = Field(default=None, foreign_key="unidades.id")
    familia_id: Optional[int] = Field(default=None, foreign_key="familias.id")
    subfamilia_id: Optional[int] = Field(default=None, foreign_key="subfamilias.id")
    rubro_insumo_id: Optional[int] = Field(default=None, foreign_key="rubro_insumos.id")
    tipo_erogacion_id: Optional[int] = Field(default=None, foreign_key="tipo_erogaciones.id")

class Insumo(InsumoBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True