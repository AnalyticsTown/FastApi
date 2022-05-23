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
    establecimiento = db.query(models.Alta_establecimiento_modelo).filter_by(
        id=almacen.establecimiento_id).first()

    db_almacen = models.Alta_almacen_modelo(**{
        "nombre": almacen.nombre,
        "abreviatura": almacen.abreviatura,
        "descripcion": almacen.descripcion,
        "geoposicion": almacen.descripcion,
        "observaciones": almacen.observaciones,
        "almacenes_tipo_id": almacen.almacenes_tipo_id
    })
    db.add(db_almacen)
    db_almacen.establecimientos.append(establecimiento)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen
