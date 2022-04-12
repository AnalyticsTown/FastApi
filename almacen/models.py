from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db.database import Base

class Alta_almacen_modelo(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    geoposicion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    almacenes_tipo_id = Column(Integer, ForeignKey("tipo_almacenes.id"), nullable=True)
    establecimiento_id = Column(Integer, ForeignKey("establecimientos.id"), nullable=True)

    #tipos = relationship("Tipo_almacen_modelo", back_populates="almacenes_tipo")

class Tipo_almacen_modelo(Base):
    __tablename__ = "tipo_almacenes"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=False)
    
    #almacenes_tipo = relationship("Alta_almacen_modelo", back_populates="tipos")