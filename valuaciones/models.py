from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import datetime
import uuid



class Insumos_valorizacion(Base):
    __tablename__ = 'insumos_valorizacion'
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    precio_total = Column(Integer, nullable=False)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=False)
    #movimiento_entrada = Column(Integer, nullable=True)
    #movimiento_salida = Column(Integer, nullable=True) 
    movimiento = Column(String, nullable=True)