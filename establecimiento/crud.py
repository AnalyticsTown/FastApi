from sqlalchemy.orm import Session

from establecimiento import models, schemas

def get_zonas(db: Session):
    return db.query(models.Zona_modelo).all()

def get_tipo_establecimientos(db: Session):
    return db.query(models.Tipo_establecimiento_modelo).all()

def get_establecimientos(db: Session):
    return db.query(models.Alta_establecimiento_modelo).all()

def get_establecimiento(db: Session, localidad: str, nombre: str):
    return db.query(models.Alta_establecimiento_modelo).filter(models.Alta_establecimiento_modelo.localidad == localidad).filter(models.Alta_establecimiento_modelo.nombre == nombre).first()

def drop_establecimientos(db: Session):
    db.query(models.Alta_establecimiento_modelo).delete()
    db.commit()

def create_establecimiento(db: Session, establecimiento: schemas.EstablecimientoBase):
    db_establecimiento = models.Alta_establecimiento_modelo(**establecimiento.dict())
    db.add(db_establecimiento)
    db.commit()
    db.refresh(db_establecimiento)
    return db_establecimiento