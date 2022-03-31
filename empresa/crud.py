from sqlalchemy.orm import Session

from empresa import models, schemas

def get_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alta_empresa_modelo).offset(skip).limit(limit).all()

def get_empresa(db: Session, razon: str, pais: str):
    return db.query(models.Alta_empresa_modelo).filter(models.Alta_empresa_modelo.razon_social == razon).filter(models.Alta_empresa_modelo.direccion_pais == pais).first()

def drop_empresas(db: Session):
    db.query(models.Alta_empresa_modelo).delete()
    db.commit()

def create_empresa(db: Session, empresa: schemas.EmpresaBase):
    db_empresa = models.Alta_empresa_modelo(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa