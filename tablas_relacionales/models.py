from sqlalchemy import Column, Integer, String, ForeignKey

from db.database import Base
from insumo.models import Encabezado_insumos_modelo, Movimiento_detalle_modelo

class Alta_inquilino_modelo(Base):
    __tablename__ = "inquilinos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    empresas = Column(String, nullable=True)
    usuarios = Column(String, nullable=True)
    accesos_por_rol = Column(String, nullable=True)

class Usuario_empresa_modelo(Base):
    __tablename__ = "usuarios_empresas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, unique=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True, unique=True)

class Establecimiento_almacen_modelo(Base):
    __tablename__ = "establecimiento_almacenes"

    id = Column(Integer, primary_key=True, index=True)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"), nullable=True, unique=True)
    establecimiento_id = Column(Integer, ForeignKey("establecimientos.id"), nullable=True, unique=True)
    
# class Encabezado_detalles(Base):
#     __tablename__ = 'encabezado_detalles'
#     id = Column(Integer, primary_key=True, index=True)
#     encabezado_id = Column(Integer, ForeignKey(Encabezado_insumos_modelo.id), nullable=False)
#     detalle_movimiento = Column(Integer, ForeignKey(Movimiento_detalle_modelo.id), nullable=False)