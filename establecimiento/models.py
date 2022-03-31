from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from db.database import Base

class Alta_establecimiento_modelo(Base):
    __tablename__ = "establecimientos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    establecimiento_tipo_id = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    localidad = Column(String, nullable=True)
    provincia = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    latitud = Column(String, nullable=True)
    longitud = Column(String, nullable=True)
    zona_id = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)