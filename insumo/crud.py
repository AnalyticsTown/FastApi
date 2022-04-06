from sqlalchemy.orm import Session

from insumo import models, schemas

def get_insumos(db: Session):
    return db.query(models.Alta_insumo_modelo).all()

def get_insumo(db: Session, nombre: str):
    return db.query(models.Alta_insumo_modelo).filter(models.Alta_insumo_modelo.nombre == nombre).first()

def drop_insumos(db: Session):
    db.query(models.Alta_insumo_modelo).delete()
    db.commit()

def create_insumo(db: Session, insumo: schemas.InsumoBase):
    db_insumo = models.Alta_insumo_modelo(**insumo.dict())
    db.add(db_insumo)
    db.commit()
    db.refresh(db_insumo)
    return db_insumo