from establecimiento.schemas import *
from establecimiento.models import *
from establecimiento.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal

establecimiento = APIRouter()

@establecimiento.get("/{empresa_id}/establecimientos/", tags=['ESTABLECIMIENTO'])
async def read_establecimientos(empresa_id: int, db: Session = Depends(get_db)):
    establecimientos = get_establecimientos(db, empresa=empresa_id)
    return JSONResponse(jsonable_encoder(establecimientos))


@establecimiento.post("/{empresa_id}/create_establecimientos/", response_model=Establecimiento, status_code=status.HTTP_201_CREATED, tags=['ESTABLECIMIENTO'])
def crear_establecimiento(empresa_id: int, establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    db_establecimiento = get_establecimiento(
        db, localidad=establecimiento.localidad, nombre=establecimiento.nombre)
    if db_establecimiento:
        raise HTTPException(
            status_code=400, detail="El establecimiento ya existe!")
    return create_establecimiento(db=db, establecimiento=establecimiento, empresa_id=empresa_id)


@establecimiento.delete("/delete_establecimientos/", tags=['ESTABLECIMIENTO'])
def delete_establecimientos(db: Session = Depends(get_db)):
    drop_establecimientos(db)
    return "Los establecimientos fueron borrados"


@establecimiento.get("/establecimiento/zonas/", response_model=list[Zona], tags=['ESTABLECIMIENTO'])
def read_zonas(db: Session = Depends(get_db)):
    zonas = get_zonas(db)
    return zonas


@establecimiento.get("/establecimiento/tipo_establecimientos/", response_model=list[TipoEstablecimiento], tags=['ESTABLECIMIENTO'])
def read_tipo_establecimientos(db: Session = Depends(get_db)):
    tipo_establecimientos = get_tipo_establecimientos(db)
    return tipo_establecimientos
