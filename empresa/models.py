from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean
from admin.models import Alta_admin_modelo
from db.database import Base
from valuaciones.models import *
from sqlalchemy.sql import func

class Alta_cond_IVA_modelo(Base):
    __tablename__ = "cond_ivas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_cond_iva = Column(String, nullable=False)

class Alta_moneda_modelo(Base):
    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_moneda = Column(String, nullable=False)

class Alta_rubro_empresa_modelo(Base):
    __tablename__ = "rubro_empresas"

    id = Column(Integer, primary_key=True, index=True)
    detalle_rubro_empresa = Column(String, nullable=False)

class Alta_empresa_modelo(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    #nombre = Column(String(60), nullable=False)
    activo = Column(Boolean, default=True)
    razon_social = Column(String(50), nullable=False)
    direccion_calle = Column(String(50), nullable=False)
    direccion_nro = Column(String, nullable=False)
    direccion_localidad = Column(String, nullable=False)
    direccion_provincia = Column(String, nullable=False)
    direccion_pais = Column(String, nullable=False)
    direccion_cod_postal = Column(String, nullable=False)
    cuit = Column(Integer, nullable=True)
    fecha_cierre = Column(Date, nullable=False)
    cond_iva_id = Column(Integer, ForeignKey("cond_ivas.id"), nullable=True)
    moneda_primaria_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)
    moneda_secundaria_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)
    rubro_empresa_id = Column(Integer, ForeignKey("rubro_empresas.id"), nullable=True)
    admin_id = Column(String, ForeignKey(Alta_admin_modelo.id_token), nullable=False)

    
    # Se agrego este campo timestamps    
    # created_at = Column(DateTime(timezone=True), default=func.now())
    # update_at = Column(DateTime(timezone=True), onupdate=func.now())
    # delete_at = Column(DateTime, nullable=True)

    
    