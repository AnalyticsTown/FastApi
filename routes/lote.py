from lote.schemas import *
from lote.models import *
from lote.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal

lote = APIRouter()


@lote.get("/lotes/", response_model=list[Lote], tags=['LOTE'])
def read_lotes(db: Session = Depends(get_db)):
    lotes = get_lotes(db)
    return lotes


@lote.post("/create_lotes/", response_model=Lote, status_code=status.HTTP_201_CREATED, tags=['LOTE'])
def crear_lote(lote: LoteBase, db: Session = Depends(get_db)):
    db_lote = get_lote(db, codigo=lote.codigo)
    if db_lote:
        raise HTTPException(status_code=400, detail="El lote ya existe!")
    return create_lote(db=db, lote=lote)


@lote.delete("/delete_lotes/", tags=['LOTE'])
def delete_lotes(db: Session = Depends(get_db)):
    drop_lotes(db)
    return "Los lotes fueron borrados"
