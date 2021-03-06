from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from modules.tablas_relacionales.models import *
from sqlalchemy.orm import relationship
from db.database import Base
import datetime

class Tipo_almacen_modelo(Base):
    __tablename__ = "tipo_almacenes"

    id = Column(Integer, primary_key=True, index=True)
    detalle_tipo_almacen = Column(String, nullable=False)


class Alta_almacen_modelo(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    geoposicion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    almacenes_tipo_id = Column(Integer, ForeignKey(
        "tipo_almacenes.id"), nullable=True)
    establecimientos = relationship(
        "Alta_establecimiento_modelo", secondary='establecimiento_almacenes', overlaps="almacenes")
    created_at = Column(DateTime(timezone=True),
                        default=datetime.datetime.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    