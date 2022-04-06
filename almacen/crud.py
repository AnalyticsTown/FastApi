from sqlalchemy.orm import Session

from almacen import models, schemas

def get_almacenes(db: Session):
    return db.query(models.Alta_almacen_modelo).all()

def get_almacen(db: Session, nombre: str, establecimiento_id: int):
    return db.query(models.Alta_almacen_modelo).filter(models.Alta_almacen_modelo.nombre == nombre).filter(models.Alta_almacen_modelo.establecimiento_id == establecimiento_id).first()

def drop_almacenes(db: Session):
    db.query(models.Alta_almacen_modelo).delete()
    db.commit()

def create_almacen(db: Session, almacen: schemas.AlmacenBase):
    db_almacen = models.Alta_almacen_modelo(**almacen.dict())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen