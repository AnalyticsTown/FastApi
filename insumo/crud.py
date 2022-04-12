from sqlalchemy.orm import Session

from insumo import models, schemas

def get_tareas(db: Session):
    return db.query(models.Alta_tarea_modelo).all()

def get_unidades(db: Session):
    return db.query(models.Alta_unidad_modelo).all()

def get_familias(db: Session):
    return db.query(models.Alta_familia_modelo).all()

def get_subfamilias(db: Session):
    return db.query(models.Alta_subfamilia_modelo).all()

def get_rubro_insumos(db: Session):
    return db.query(models.Alta_rubro_insumo_modelo).all()

def get_tipo_erogaciones(db: Session):
    return db.query(models.Alta_erogacion_modelo).all()

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