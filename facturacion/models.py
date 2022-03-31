from datetime import date
from sqlalchemy import Column, Integer, String, Date

from db.database import Base

class Alta_facturacion_modelo(Base):
    __tablename__ = "facturaciones"

    id = Column(Integer, primary_key=True, index=True)
    tarjeta_emisor_id = Column(String, nullable=True)
    nro_tarjeta = Column(Integer, nullable=True)
    vto_fecha = Column(Date, nullable=True)
    cod_verificacion = Column(Integer, nullable=True)
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)