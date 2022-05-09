from almacen.schemas import *
from almacen.models import *
from almacen.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal

almacen = APIRouter()

# ALMACEN
@almacen.get("/almacenes/", tags=['ALMACEN'])
def read_almacenes(db: Session = Depends(get_db)):
    almacenes = get_almacenes(db)
    return JSONResponse(jsonable_encoder(almacenes))


@almacen.post("/create_almacenes/", response_model=AlmacenBase, status_code=status.HTTP_201_CREATED, tags=['ALMACEN'])
def crear_almacen(almacen: AlmacenBase, db: Session = Depends(get_db)):
    db_almacen = get_almacen(db, nombre=almacen.nombre)
    if db_almacen:
        raise HTTPException(status_code=400, detail="El almacen ya existe!")
    return create_almacen(db=db, almacen=almacen)

@almacen.delete("/delete_almacenes/", tags=['ALMACEN'])
def delete_almacenes(db: Session = Depends(get_db)):
    drop_almacenes(db)
    return "Los almacenes fueron borrados"


@almacen.get("/almacen/tipo_almacenes/", response_model=list[TipoAlmacen], tags=['ALMACEN'])
def read_tipo_almacenes(db: Session = Depends(get_db)):
    tipo_almacenes = get_tipo_almacenes(db)
    return tipo_almacenes
