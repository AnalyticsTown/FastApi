from datetime import date
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from modules.empresa.models import Alta_empresa_modelo
from modules.tablas_relacionales.models import *
from db.database import Base

class Alta_rol_modelo(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    detalle_rol = Column(String, nullable=True)

class Alta_auditoria_modelo(Base):
    __tablename__ = "log_auditoria_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=True)
    criticidad = Column(String, nullable=True)
    detalle = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

class Alta_usuario_modelo(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    dni = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    activo = Column(Boolean, default=True)
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    empresa_id = Column(Integer, ForeignKey(Alta_empresa_modelo.id), nullable=False)
    