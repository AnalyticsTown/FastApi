from sqlalchemy.orm import Session
from almacen.models import Alta_almacen_modelo

from establecimiento import models, schemas


def get_zonas(db: Session):
    return db.query(models.Zona_modelo).all()


def get_tipo_establecimientos(db: Session):
    return db.query(models.Tipo_establecimiento_modelo).all()

# def get_establecimientos(db: Session):
#     return db.query(models.Alta_establecimiento_modelo).all()


def get_establecimientos(db: Session, empresa: int):
    statement = """select establecimientos.id, activo, nombre, abreviatura, direccion, localidad, provincia, pais, 
                   geoposicion, observaciones, contacto, detalle_zona, detalle_tipo_establecimiento, empresa_id
                   from establecimientos
                   left join zonas on establecimientos.zona_id = zonas.id
                   left join tipo_establecimientos on tipo_establecimientos.id = establecimientos.establecimiento_tipo_id
                   where empresa_id = {empresa}""".format(empresa=empresa)

    return db.execute(statement).all()


def get_establecimiento(db: Session, localidad: str, nombre: str):
    return db.query(models.Alta_establecimiento_modelo).filter(models.Alta_establecimiento_modelo.localidad == localidad).filter(models.Alta_establecimiento_modelo.nombre == nombre).first()


def drop_establecimientos(db: Session):
    db.query(models.Alta_establecimiento_modelo).delete()
    db.commit()


def create_establecimiento(db: Session, establecimiento: schemas.Establecimiento, empresa_id: int):
    almacen = db.query(Alta_almacen_modelo).filter_by(
        id=establecimiento.almacen_id).first()
    db_establecimiento = models.Alta_establecimiento_modelo(**{
        "nombre": establecimiento.nombre,
        "abreviatura": establecimiento.abreviatura,
        "direccion": establecimiento.direccion,
        "localidad": establecimiento.localidad,
        "provincia": establecimiento.provincia,
        "pais": establecimiento.pais,
        "geoposicion": establecimiento.geoposicion,
        "observaciones": establecimiento.observaciones,
        "contacto": establecimiento.contacto,
        "zona_id": establecimiento.zona_id,
        "establecimiento_tipo_id": establecimiento.establecimiento_tipo_id,
    }, empresa_id=empresa_id)
    db.add(db_establecimiento)
    if establecimiento.almacen_id:
        db_establecimiento.almacenes.append(almacen)
    
    db.commit()
    db.refresh(db_establecimiento)
    return db_establecimiento
