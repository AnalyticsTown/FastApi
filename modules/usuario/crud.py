from sqlalchemy.orm import Session
from modules.usuario import models, schemas


def crear_empleado(db: Session, empleado: schemas.Usuario):
    db_empleado = models.Alta_admin_modelo(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

def get_usuario(db: Session, email: str):
    return db.query(models.Alta_usuario_modelo).filter(models.Alta_usuario_modelo.email == email).first()
