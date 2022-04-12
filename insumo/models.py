from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date

from db.database import Base

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
    reposicion_cantidad = Column(Integer, nullable=True)
    reposicion_alerta = Column(Boolean, nullable=True)
    reposicion_alerta_email = Column(String, nullable=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=True)
    subfamilia_id = Column(Integer, ForeignKey("subfamilias.id"), nullable=True)
    rubro_insumo_id = Column(Integer, ForeignKey("rubro_insumos.id"), nullable=True)
    tipo_erogacion_id = Column(Integer, ForeignKey("tipo_erogaciones.id"), nullable=True)

class Alta_tarea_modelo(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)

class Alta_erogacion_modelo(Base):
    __tablename__ = "tipo_erogaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)

class Alta_unidad_modelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)

class Alta_familia_modelo(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)

class Alta_subfamilia_modelo(Base):
    __tablename__ = "subfamilias"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)

class Alta_rubro_insumo_modelo(Base):
    __tablename__ = "rubro_insumos"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)