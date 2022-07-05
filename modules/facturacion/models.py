from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

from db.database import Base

class Alta_tarjeta_emisor_modelo(Base):
    __tablename__ = "emisor_tarjetas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_emisor_tarjeta = Column(String, nullable=True)

class Alta_facturacion_modelo(Base):
    __tablename__ = "facturaciones"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    nro_tarjeta = Column(Integer, nullable=True)
    vto_fecha = Column(Date, nullable=True)
    cod_verificacion = Column(Integer, nullable=True)
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)
    tarjeta_emisor_id = Column(Integer, ForeignKey("emisor_tarjetas.id"), nullable=True)