from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.database import Base

class Alta_empresa_modelo(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String, nullable=False)
    direccion_calle = Column(String, nullable=False)
    direccion_nro = Column(String, nullable=False)
    direccion_localidad = Column(String, nullable=False)
    direccion_provincia = Column(String, nullable=False)
    direccion_pais = Column(String, nullable=False)
    direccion_cod_postal = Column(String, nullable=False)
    cuit = Column(Integer, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario_empresas.usuario_id"), nullable=True)
    cond_iva_id = Column(Integer, ForeignKey("cond_ivas.id"), nullable=True)
    rubro_empresa_id = Column(Integer, ForeignKey("rubro_empresas.id"))
    fecha_cierre = Column(Date, nullable=False)
    moneda_primaria_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)
    moneda_secundaria_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)

    establecimientos = relationship("Alta_establecimiento_modelo", back_populates="id")

class Alta_cond_IVA_modelo(Base):
    __tablename__ = "cond_ivas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_rubro_empresa_modelo(Base):
    __tablename__ = "rubro_empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)

class Alta_moneda_modelo(Base):
    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)
