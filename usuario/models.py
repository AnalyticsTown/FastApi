from datetime import date, datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, DateTime

from db.database import Base

class Alta_usuario_modelo(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    dni = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    activo = Column(Boolean, default=True)
    empresa_id = Column(Integer, ForeignKey("usuario_empresas.empresa_id"))
    rol_id = Column(Integer, ForeignKey("roles.id"))
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)

class Alta_rol_modelo(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    rol_descripcion = Column(String, nullable=True)
    tipo_acceso_id = Column(Integer, ForeignKey("tipo_accesos.id"), nullable=True)
    menu_acceso = Column(String, nullable=True)

class Alta_auditoria_modelo(Base):
    __tablename__ = "log_auditoria_usuarios"

    id_urs = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(Date, nullable=True)
    tipo_de_accion = Column(String, nullable=True)
    tabla_modificada = Column(String, nullable=True)
    registro_modificado = Column(String, nullable=True)

class Alta_accesos_modelo(Base):
    __tablename__ = "tipo_accesos"

    id = Column(Integer, primary_key=True, index=True)
    permisos = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)