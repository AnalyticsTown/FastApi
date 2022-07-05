from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean
from db.database import Base


class Alta_admin_modelo(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    id_token = Column(String, nullable=False, unique=True)
