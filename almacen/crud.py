from sqlalchemy.orm import Session

from almacen import models, schemas

def get_tipo_almacenes(db: Session):
    return db.query(models.Tipo_almacen_modelo).all()

def get_almacenes(db: Session):
    statement = """select almacenes.id, 
                   activo, 
                   nombre, 
                   abreviatura, 
                   descripcion, 
                   geoposicion, 
                   observaciones, 
                   detalle_tipo_almacen
                   from almacenes
                   inner join tipo_almacenes on tipo_almacenes.id = almacenes.almacenes_tipo_id"""

    return db.execute(statement).all()

def get_almacen(db: Session, nombre: str):
    return db.query(models.Alta_almacen_modelo).filter(models.Alta_almacen_modelo.nombre == nombre).first()

def drop_almacenes(db: Session):
    db.query(models.Alta_almacen_modelo).delete()
    db.commit()

def create_almacen(db: Session, almacen: schemas.AlmacenBase):
    db_almacen = models.Alta_almacen_modelo(**almacen.dict())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen