from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import FetchedValue


class Tarea(BaseModel):
    id: int
    detalle_tarea: str

    class Config:
        orm_mode = True


class Unidad(BaseModel):
    id: int
    abr: str

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


# class LoteInsumo(BaseModel):
#     id: int
#     nro_lote: str
#     fecha_vencimiento: date
#     stock_id: Optional[int] = Field(
#         default=None, foreign_key="stocks.id")

#     class Config:
#         orm_mode = True


class TipoMovimientoInsumo(BaseModel):
    id: int
    detalle_tipo_movimiento_insumo: str

    class Config:
        orm_mode = True


class EncabezadoInsumos(BaseModel):
    
    tipo_movimiento_id: int
    fecha_valor: date
    fecha_real: date
    origen_almacen_id: Optional[int] = None
    destino_almacen_id: Optional[int] 
    orden_de_compra: Optional[str] = None
    nro_movimiento: str
    
    class Config:
        orm_mode = True


class MovimientoDetalleBase(BaseModel):

    insumo_id: int
    cantidad: float
    nro_lote: Optional[str] = None 
    fecha_vencimiento: Optional[date] = None
    precio_unitario: Optional[float] = None
    observaciones: Optional[str] = None
    encabezado_movimiento_id: str
    precio_total: Optional[float] = None
    class Config:
        orm_mode = True


class MovimientoDetalle(MovimientoDetalleBase):
    id: int

    class Config:
        orm_mode = True


class StockAlmacenInsumoBase(BaseModel):
    detalle: Optional[str]
    cantidad: Optional[float]
    insumo_id: Optional[int] #= Field(default=None, foreign_key="insumos.id")
    almacen_id: Optional[int] #= Field(default=None, foreign_key="almacenes.id")
    nro_lote: Optional[str]
    fecha_vencimiento: Optional[str]
    reposicion_cantidad: Optional[float]
    reposicion_alerta: Optional[bool]
    unidad_id: Optional[int]
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
    # Se agrego este campo. Viene de la tabla stocks
    reposicion_cantidad: Optional[float]
    reposicion_alerta: Optional[bool]
    # Se agrego este campo. Viene de la tabla stocks
    reposicion_alerta_email: Optional[EmailStr]
    tarea_id: Optional[int] = Field(default=None, foreign_key="tareas.id")
    unidad_id: Optional[int] = Field(default=None, foreign_key="unidades.id")
    familia_id: Optional[int] = Field(default=None, foreign_key="familias.id")
    subfamilia_id: Optional[int] = Field(
        default=None, foreign_key="subfamilias.id")
    rubro_insumo_id: Optional[int] = Field(
        default=None, foreign_key="rubro_insumos.id")
    tipo_erogacion_id: Optional[int] = Field(
        default=None, foreign_key="tipo_erogaciones.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    

class Insumo(InsumoBase):
    id: int
    activo: bool
    
    class Config:
        orm_mode = True
