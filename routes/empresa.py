from modules.empresa.schemas import *
from modules.empresa.models import *
from modules.empresa.crud import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import  Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db

empresa = APIRouter()
##############################################################################################################
################################################ CRUD EMPRESA ################################################
##############################################################################################################


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


@empresa.put("/update_empresa/", tags=['EMPRESA'])
def update_empresa(id: int, empresa: EmpresaBase, db: Session = Depends(get_db)):
    try:
        db.query(Alta_empresa_modelo).filter_by(id=id).\
            update({
                Alta_empresa_modelo.razon_social: empresa.razon_social,
                Alta_empresa_modelo.direccion_calle: empresa.direccion_calle,
                Alta_empresa_modelo.direccion_nro: empresa.direccion_nro,
                Alta_empresa_modelo.direccion_localidad: empresa.direccion_localidad,
                Alta_empresa_modelo.direccion_pais: empresa.direccion_pais,
                Alta_empresa_modelo.direccion_cod_postal: empresa.direccion_cod_postal,
                Alta_empresa_modelo.cuit: empresa.cuit,
                Alta_empresa_modelo.fecha_cierre: empresa.fecha_cierre,
                Alta_empresa_modelo.cond_iva_id: empresa.cond_iva_id,
                Alta_empresa_modelo.moneda_primaria_id: empresa.moneda_primaria_id,
                Alta_empresa_modelo.moneda_secundaria_id: empresa.moneda_secundaria_id,
                Alta_empresa_modelo.rubro_empresa_id: empresa.rubro_empresa_id
            })
        db.commit()
        return JSONResponse({"response": "Empresa actualizada exitosamente"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({"response": "Ocurrió un error"}, status_code=500)


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

#################################################((***))######################################################
