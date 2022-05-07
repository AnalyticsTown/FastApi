from sqlalchemy.orm import Session
from admin import models, schemas

def create_admin(db: Session, admin: schemas.Admin_base):
    db_admin = models.Alta_admin_modelo(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    
    


