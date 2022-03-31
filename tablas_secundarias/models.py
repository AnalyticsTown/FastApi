from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from db.database import Base

class Alta_inquilino_modelo(Base):
    __tablename__ = "inquilinos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    empresas = Column(String, nullable=True)
    usuarios = Column(String, nullable=True)
    accesos_por_rol = Column(String, nullable=True)

class Alta_rol_modelo(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    rol_descripcion = Column(String, nullable=True)
    tipo_acceso_id = Column(String, nullable=True)
    menu_acceso = Column(String, nullable=True)

class Alta_auditoria_modelo(Base):
    __tablename__ = "log_auditoria_usuarios"

    id_urs = Column(Integer, primary_key=True, index=True)
    tipo_de_accion = Column(String, nullable=True)
    tabla_modificada = Column(String, nullable=True)
    registro_modificado = Column(String, nullable=True)

class Alta_erogacion_modelo(Base):
    __tablename__ = "tipo_erogaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    abreviatura = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)


class Alta_unidad_modelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)


class Alta_rubro_modelo(Base):
    __tablename__ = "rubros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_familia_modelo(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_subfamilia_modelo(Base):
    __tablename__ = "subfamilias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)