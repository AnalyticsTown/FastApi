from sqlalchemy import Column, Integer, String, Date, ForeignKey

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
    cond_iva_id = Column(String, nullable=True)
    rubro_id = Column(Integer, ForeignKey("rubros.id"), nullable=True)
    fecha_cierre = Column(Date, nullable=False)
    moneda_primaria_id = Column(String, nullable=True)
    moneda_secundaria_id = Column(String, nullable=True)
