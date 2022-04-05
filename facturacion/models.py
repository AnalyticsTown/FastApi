from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime

from db.database import Base

class Alta_facturacion_modelo(Base):
    __tablename__ = "facturaciones"

    id = Column(Integer, primary_key=True, index=True)
    tarjeta_emisor_id = Column(Integer, ForeignKey("emisor_tarjetas.id"), nullable=True)
    nro_tarjeta = Column(Integer, nullable=True)
    vto_fecha = Column(Date, nullable=True)
    cod_verificacion = Column(Integer, nullable=True)
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)

class Alta_tarjeta_emisor_modelo(Base):
    __tablename__ = "emisor_tarjetas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)