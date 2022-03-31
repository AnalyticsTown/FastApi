from datetime import date
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey

from db.database import Base

class Alta_usuario_modelo(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    dni = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    activo = Column(Boolean, default=True)
    empresa = Column(Integer, ForeignKey("empresas.id"))
    rol_id = Column(Integer, ForeignKey("roles.id"))
    fecha_alta = Column(Date, default=date.today)
    fecha_baja = Column(Date, nullable=True)