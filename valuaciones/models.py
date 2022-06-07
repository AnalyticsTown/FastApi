from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import datetime
import uuid



class Insumos_valorizacion(Base):
    __tablename__ = 'insumos_valorizacion'
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    precio_total = Column(Integer, nullable=False)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=False) 
    movimiento = Column(String, nullable=True)
    tipo_movimiento_id = Column(Integer, ForeignKey("tipo_movimiento_insumos.id"))
    insumo_id = Column(Integer, ForeignKey("insumos.id"))
    
class Tipo_Metodo_Valorizacion(Base):
    __tablename__ = 'tipo_metodo_valorizacion'
    id = Column(Integer, primary_key=True, nullable=False)
    abreviatura = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    
    