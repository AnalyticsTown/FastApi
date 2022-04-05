from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from db.database import Base

class Usuario_empresa_modelo(Base):
    __tablename__ = "usuario_empresas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

class Alta_inquilino_modelo(Base):
    __tablename__ = "inquilinos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    empresas = Column(String, nullable=True)
    usuarios = Column(String, nullable=True)
    accesos_por_rol = Column(String, nullable=True)