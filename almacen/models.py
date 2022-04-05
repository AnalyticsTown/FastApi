from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from db.database import Base

class Alta_almacen_modelo(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    establecimiento_id = Column(Integer, ForeignKey("establecimientos.id"))
    almacenes_tipo_id = Column(Integer, ForeignKey("tipo_almacenes.id"))
    geoposicion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Tipo_almacen_modelo(Base):
    __tablename__ = "tipo_almacenes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)