from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

from db.database import Base

class Alta_lote_modelo(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False)
    establecimiento_id = Column(Integer, ForeignKey("establecimientos.id"), nullable=True)
    superficie = Column(Float, nullable=True)
    poligono = Column(Float, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted = Column(DateTime, nullable=True)
