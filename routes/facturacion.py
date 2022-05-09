from facturacion.schemas import *
from facturacion.models import *
from facturacion.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal

facturacion = APIRouter()

#FACTURACION
@facturacion.get("/facturaciones/", response_model=list[Facturacion], tags=['FACTURACION'])
def read_facturaciones(db: Session = Depends(get_db)):
    facturaciones = get_facturaciones(db)
    return facturaciones

@facturacion.post("/create_facturaciones/", response_model=Facturacion, status_code=status.HTTP_201_CREATED, tags=['FACTURACION'])
def crear_facturacion(facturacion: FacturacionBase, db: Session = Depends(get_db)):
    db_facturacion = get_facturacion(db, nro_tarjeta=facturacion.nro_tarjeta)
    if db_facturacion:
        raise HTTPException(status_code=400, detail="La tarjeta ya existe!")
    return create_facturacion(db=db, facturacion=facturacion)

@facturacion.delete("/delete_facturaciones/", tags=['FACTURACION'])
def delete_facturaciones(db: Session = Depends(get_db)):
    drop_facturaciones(db)
    return "Las facturaciones fueron borradas"
