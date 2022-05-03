import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Float

from db.database import Base

class Alta_tarea_modelo(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tarea = Column(String, nullable=False)

class Alta_unidad_modelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    detalle_unidad = Column(String, nullable=False)

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

class Lote_insumo_modelo(Base):
    __tablename__ = "lote_insumos"

    id = Column(Integer, primary_key=True, index=True)
    nro_lote = Column(String, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    stock_id = Column(Integer, ForeignKey("stock_almacen_insumos.id"), nullable=True)

class Alta_tipo_movimiento_modelo(Base):
    __tablename__ = "tipo_movimiento_insumos"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tipo_movimiento_insumo = Column(String)

class Moviemiento_insumos_modelo(Base):
    __tablename__ = "movimiento_insumos"

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float)
    fecha_movimiento = Column(Date)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=True)
    origen_almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=True)
    destino_almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=True)
    tipo_movimiento_id = Column(Integer, ForeignKey("tipo_movimiento_insumos.id"), nullable=True)

    created_at = Column(Date, default=datetime.datetime.utcnow().date())

class Stock_almacen_insumo_modelo(Base):
    __tablename__ = "stock_almacen_insumos"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=True)
    cantidad = Column(Float, nullable=False)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=True)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=True)
    # Falta un campo reposicion control id y reposicion alerta id que sean FK a insumos (el maestro)

class Alta_insumo_modelo(Base):
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    codigo_externo = Column(String, nullable=True)
    lote_control = Column(Boolean, nullable=True)
    vencimiento_control = Column(Boolean, nullable=True)
    reposicion_control = Column(Boolean, nullable=True)
    reposicion_cantidad = Column(Float, nullable=True) # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    reposicion_alerta = Column(Boolean, nullable=True)
    reposicion_alerta_email = Column(String, nullable=True) # Se agrego este campo. Viene de la tabla stock_almacen_insumos
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=True)
    subfamilia_id = Column(Integer, ForeignKey("subfamilias.id"), nullable=True)
    rubro_insumo_id = Column(Integer, ForeignKey("rubro_insumos.id"), nullable=True)
    tipo_erogacion_id = Column(Integer, ForeignKey("tipo_erogaciones.id"), nullable=True)