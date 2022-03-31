# from sqlalchemy.orm import Session
#
# from usuario import models, schemas
#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.Alta_usuario_modelo).filter(models.Alta_usuario_modelo.email == email).first()
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Alta_usuario_modelo).offset(skip).limit(limit).all()
#
# def create_user(db: Session, user: schemas.Alta_usuario_schema):
#     fake_hashed_password = user.contraseña + "notreallyhashed"
#     db_user = models.Alta_usuario_modelo(email=user.email,
#                                          contraseña=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user