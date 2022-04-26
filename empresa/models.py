from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

from db.database import Base

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

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    razon_social = Column(String, nullable=False)
    direccion_calle = Column(String, nullable=False)
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
    usuario_id = Column(Integer, ForeignKey("usuario_empresas.usuario_id"), nullable=True)