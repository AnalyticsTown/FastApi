from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, get_db, Base
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.exception_handlers import request_validation_exception_handler
import json
from starlette.responses import JSONResponse

#%% Es para crear la base de datos. Importo todos los modelos
from empresa.models import *
from usuario.models import *
from establecimiento.models import *
from almacen.models import *
from insumo.models import *
from facturacion.models import *
from tablas_secundarias.models import *
#%%

from empresa.schemas import *
from empresa.crud import *
from establecimiento.schemas import *
from establecimiento.crud import *
# from usuario.schemas import Alta_usuario_schema
# from usuario.crud import get_user_by_email, get_users#, get_user, create_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

# @app.exception_handler(ValueError)
# async def value_error_exception_handler(request: Request, exc: ValueError):
#     return JSONResponse(status_code=400, content={"message": str(exc)})

@app.post("/create_empresas/", response_model=Empresa, status_code=status.HTTP_201_CREATED)
def crear_empresa(empresa: EmpresaBase, db: Session = Depends(get_db)):
    db_empresa = get_empresa(db, razon=empresa.razon_social, pais=empresa.direccion_pais)
    if db_empresa:
        raise HTTPException(status_code=400, detail="La empresa ya existe!")
    return create_empresa(db=db, empresa=empresa)

@app.get("/empresas/", response_model=list[Empresa])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empresas = get_empresas(db, skip=skip, limit=limit)
    return empresas

@app.delete("/delete_empresas")
def delete_empresas(db: Session = Depends(get_db)):
    drop_empresas(db)
    return "Las empresas fueron borradas"

@app.post("/create_establecimientos/", response_model=Establecimiento, status_code=status.HTTP_201_CREATED)
def crear_establecimiento(establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    db_establecimiento = get_establecimiento(db, localidad=establecimiento.localidad, direccion=establecimiento.direccion)
    if db_establecimiento:
        raise HTTPException(status_code=400, detail="El establecimiento ya existe!")
    return create_establecimiento(db=db, establecimiento=establecimiento)

@app.get("/establecimientos/", response_model=list[Establecimiento])
def read_establecimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    establecimientos = get_establecimientos(db, skip=skip, limit=limit)
    return establecimientos

@app.delete("/delete_establecimientos")
def delete_establecimientos(db: Session = Depends(get_db)):
    drop_establecimientos(db)
    return "Los establecimientos fueron borrados"