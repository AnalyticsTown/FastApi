# from pydantic import BaseModel
#
#
# class UserBase(BaseModel):   # Esto es una secuencia. Se pide el email, luego el password y por ultimo los otros datos
#     email: str
#
# class UserCreate(UserBase):
#     password: str
#
# class Alta_usuario_schema(BaseModel):
#     email: str
#     contraseña: str
#     is_active: bool
#     is_staff: bool
#     nombre: str | None = None
#     apellido: str | None = None
#     dni: int | None = None
#     #empresa: str
#
#     class Config:
#         orm_mode = True