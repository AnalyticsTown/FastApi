from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from db.database import Base

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
    latitud = Column(String, nullable=True)
    longitud = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    contacto = Column(String, nullable=True)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)
    establecimiento_tipo_id = Column(Integer, ForeignKey("tipo_establecimientos.id"), nullable=True)

class Tipo_establecimiento_modelo(Base):
    __tablename__ = "tipo_establecimientos"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=True)

class Zona_modelo(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    detalle = Column(String, nullable=True)