from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
#from almacen.models import Alta_almacen_modelo

class Zona_modelo(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_zona = Column(String, nullable=True)


class Tipo_establecimiento_modelo(Base):
    __tablename__ = "tipo_establecimientos"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tipo_establecimiento = Column(String, nullable=True)


class Alta_establecimiento_modelo(Base):
    __tablename__ = "establecimientos"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    localidad = Column(String, nullable=True)
    provincia = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    # Se cambiaron los campos latitud y longitud por este
    geoposicion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    contacto = Column(String, nullable=True)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)
    establecimiento_tipo_id = Column(Integer, ForeignKey(
        "tipo_establecimientos.id"), nullable=True)
    almacenes = relationship("Alta_almacen_modelo", secondary="establecimiento_almacenes")
