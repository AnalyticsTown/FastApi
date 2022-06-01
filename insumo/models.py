from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import datetime
import uuid


class Alta_tarea_modelo(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tarea = Column(String, nullable=False)


class Alta_unidad_modelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    abr = Column(String, nullable=False)
    español = Column(String, nullable=False)
    ingles = Column(String, nullable=False)
    portugues = Column(String, nullable=False)

class Alta_familia_modelo(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    detalle_familia = Column(String, nullable=False)


class Alta_subfamilia_modelo(Base):
    __tablename__ = "subfamilias"

    id = Column(Integer, primary_key=True, index=True)
    detalle_subfamilia = Column(String, nullable=False)


class Alta_rubro_insumo_modelo(Base):
    __tablename__ = "rubro_insumos"

    id = Column(Integer, primary_key=True, index=True)
    detalle_rubro_insumo = Column(String, nullable=False)


class Alta_erogacion_modelo(Base):
    __tablename__ = "tipo_erogaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre_tipo_erogacion = Column(String, nullable=False)
    abreviatura_tipo_erogacion = Column(String, nullable=False)


# class Lote_insumo_modelo(Base):
#     __tablename__ = "lote_insumos"

#     id = Column(Integer, primary_key=True, index=True)
#     nro_lote = Column(String, nullable=True, unique=True)
#     fecha_vencimiento = Column(Date, nullable=True)
#     stock_id = Column(Integer, ForeignKey(
#         "stock_almacen_insumos.id"), nullable=True)


class Alta_tipo_movimiento_modelo(Base):
    __tablename__ = "tipo_movimiento_insumos"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tipo_movimiento_insumo = Column(String)


class Encabezado_insumos_modelo(Base):
    __tablename__ = "encabezado_movimiento"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, unique=True, default=uuid.uuid4)
    tipo_movimiento_id = Column(Integer, ForeignKey(
        Alta_tipo_movimiento_modelo.id), nullable=True)
    nro_movimiento = Column(String, nullable=False, unique=True)
    fecha_real = Column(Date, nullable=False)
    fecha_valor = Column(Date, nullable=False)
    origen_almacen_id = Column(
        Integer, ForeignKey("almacenes.id"), nullable=True)
    destino_almacen_id = Column(
        Integer, ForeignKey("almacenes.id"), nullable=True)
    orden_de_compra = Column(String(255), nullable=True)
   


class Alta_insumo_modelo(Base):
    __tablename__ = "insumos"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    activo = Column(Boolean, default=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    codigo_externo = Column(String, nullable=True)
    lote_control = Column(Boolean, nullable=True)
    vencimiento_control = Column(Boolean, nullable=True)
    reposicion_control = Column(Boolean, nullable=True)
    # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    reposicion_cantidad = Column(Float, nullable=True)
    reposicion_alerta = Column(Boolean, nullable=True)
    # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    reposicion_alerta_email = Column(String, nullable=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=True)
    subfamilia_id = Column(Integer, ForeignKey(
        "subfamilias.id"), nullable=True)
    rubro_insumo_id = Column(Integer, ForeignKey(
        "rubro_insumos.id"), nullable=True)
    tipo_erogacion_id = Column(Integer, ForeignKey(
        "tipo_erogaciones.id"), nullable=True)


class Movimiento_detalle_modelo(Base):
    __tablename__ = "movimiento_detalle"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    insumo_id = Column(Integer, ForeignKey(
        Alta_insumo_modelo.id), nullable=False)
    cantidad = Column(Float)
    unidad_id = Column(Integer, ForeignKey(
        Alta_unidad_modelo.id), nullable=True)
    nro_lote = Column(String, nullable=True)
    fecha_vencimiento = Column(Date)
    precio_unitario = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    encabezado_movimiento_id = Column(UUID, ForeignKey(
        Encabezado_insumos_modelo.id), nullable=False)
    precio_total = Column(Float, nullable=True)

class Stock_almacen_insumo_modelo(Base):
    __tablename__ = "stock_almacen_insumos"
    # INSUMO_ALMACEN
    id = Column(Integer, primary_key=True, index=True, unique=True)
    cantidad = Column(Float, nullable=False)
    detalle = Column(String, nullable=True)
    insumo_id = Column(Integer, ForeignKey(Alta_insumo_modelo.id))
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=True)
    nro_lote = Column(String(255), nullable=True)
    fecha_vencimiento = Column(String(255), nullable=True)
    unidad_id = Column(Integer, ForeignKey(
        Alta_unidad_modelo.id), nullable=False)
    precio_unitario = Column(Float, nullable=True)
    precio_total = Column(Float, nullable=True)