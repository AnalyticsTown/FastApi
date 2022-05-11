from empresa.schemas import *
from empresa.models import *
from empresa.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base, SessionLocal

empresa = APIRouter()

@empresa.get("/empresas/", tags=['EMPRESA'])
def read_empresas(db: Session = Depends(get_db)):
    empresas = get_empresas(db)
    return JSONResponse(jsonable_encoder(empresas))

@empresa.post("/create_empresas/", response_model=Empresa, status_code=status.HTTP_201_CREATED, tags=['EMPRESA'])
def crear_empresa(empresa: EmpresaBase, db: Session = Depends(get_db)):
    db_empresa = get_empresa(
        db, razon=empresa.razon_social, pais=empresa.direccion_pais)
    if db_empresa:
        raise HTTPException(status_code=400, detail="La empresa ya existe!")
    if empresa.direccion_pais.casefold() == 'argentina':
        if empresa.cuit == None:
            raise HTTPException(status_code=400, detail="Completar CUIT")
        if empresa.cond_iva_id == None:
            raise HTTPException(
                status_code=400, detail="Completar condición ante el IVA ")
    return create_empresa(db=db, empresa=empresa)


@empresa.delete("/delete_empresas/", tags=['EMPRESA'])
def delete_empresas(db: Session = Depends(get_db)):
    drop_empresas(db)
    return "Las empresas fueron borradas"


@empresa.get("/empresa/cond_ivas/", response_model=list[CondicionIva], tags=['EMPRESA'])
def read_cond_ivas(db: Session = Depends(get_db)):
    cond_ivas = get_cond_ivas(db)
    return cond_ivas


@empresa.get("/empresa/rubro_empresas/", response_model=list[RubroEmpresa], tags=['EMPRESA'])
def read_rubro_empresas(db: Session = Depends(get_db)):
    rubro_empresas = get_rubro_empresas(db)
    return rubro_empresas


@empresa.get("/empresa/monedas/", response_model=list[Moneda], tags=['EMPRESA'])
def read_monedas(db: Session = Depends(get_db)):
    monedas = get_monedas(db)
    return monedas
