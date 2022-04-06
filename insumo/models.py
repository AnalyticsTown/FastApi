from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Date

from db.database import Base

class Alta_insumo_modelo(Base):
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    codigo_externo = Column(String, nullable=True)
    lote_control = Column(Boolean, nullable=True)
    lote_numero = Column(String, nullable=True)
    vencimiento_control = Column(Boolean, nullable=True)
    vencimiento_fecha = Column(Date, nullable=True)
    reposicion_control = Column(Boolean, nullable=True)
    reposicion_cantidad = Column(Integer, nullable=True)
    reposicion_alerta = Column(String, nullable=True)
    tipo_erogacione_id = Column(Integer, ForeignKey("tipo_erogaciones.id"))
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    rubro_insumo_id = Column(Integer, ForeignKey("rubro_insumos.id"))
    familia_id = Column(Integer, ForeignKey("familias.id"))
    subfamilia_id = Column(Integer, ForeignKey("subfamilias.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_erogacion_modelo(Base):
    __tablename__ = "tipo_erogaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_unidad_modelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_familia_modelo(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_subfamilia_modelo(Base):
    __tablename__ = "subfamilias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_rubro_insumo_modelo(Base):
    __tablename__ = "rubro_insumos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)