from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean

from db.database import Base

class Alta_lote_modelo(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    activo = Column(Boolean, default=True)
    codigo = Column(String, nullable=False)
    poligono = Column(String, nullable=True)
    superficie = Column(Float, nullable=True)
    superficie_calculada = Column(Float, nullable=True)
    establecimiento_id = Column(Integer, ForeignKey("establecimientos.id"), nullable=True)
