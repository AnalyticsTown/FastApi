from sqlalchemy.orm import Session

from modules.lote import models, schemas

def get_lotes(db: Session):
    return db.query(models.Alta_lote_modelo).all()

def get_lote(db: Session, codigo: str):
    return db.query(models.Alta_lote_modelo).filter(models.Alta_lote_modelo.codigo == codigo).first()

def drop_lotes(db: Session):
    db.query(models.Alta_lote_modelo).delete()
    db.commit()

def create_lote(db: Session, lote: schemas.LoteBase):
    db_lote = models.Alta_lote_modelo(**lote.dict())
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote