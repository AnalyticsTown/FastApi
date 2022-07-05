from sqlalchemy.orm import Session

from facturacion import models, schemas

def get_facturaciones(db: Session):
    return db.query(models.Alta_facturacion_modelo).all()

def get_facturacion(db: Session, nro_tarjeta: int):
    return db.query(models.Alta_facturacion_modelo).filter(models.Alta_facturacion_modelo.nro_tarjeta == nro_tarjeta).first()

def drop_facturaciones(db: Session):
    db.query(models.Alta_facturacion_modelo).delete()
    db.commit()

def create_facturacion(db: Session, facturacion: schemas.FacturacionBase):
    db_facturacion = models.Alta_facturacion_modelo(**facturacion.dict())
    db.add(db_facturacion)
    db.commit()
    db.refresh(db_facturacion)
    return db_facturacion