import json
import random
import datetime
from this import s
from helpers.pagination import paginate
from sqlalchemy import func
from requests import session
from empresa.models import Alta_empresa_modelo
from insumo.schemas import *
from insumo.models import *
from insumo.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.database import engine, get_db, Base  # , SessionLocal
from valuaciones.crud import *
insumo = APIRouter()


##############################################################################################################
################################  DATOS DE INSUMOS DE SÓLO LECTURA   #########################################
##############################################################################################################


@insumo.get("/insumo/tareas/", response_model=list[Tarea], tags=['INSUMO'])
def read_tareas(db: Session = Depends(get_db)):
    tareas = get_tareas(db)
    return tareas


@insumo.get("/insumo/unidades/", response_model=list[Unidad], tags=['INSUMO'])
def read_unidades(db: Session = Depends(get_db)):
    unidades = get_unidades(db)
    return unidades


@insumo.get("/insumo/familias/", response_model=list[Familia], tags=['INSUMO'])
def read_familias(db: Session = Depends(get_db)):
    familias = get_familias(db)
    return familias


@insumo.get("/insumo/subfamilias/", response_model=list[Subfamilia], tags=['INSUMO'])
def read_subfamilias(db: Session = Depends(get_db)):
    subfamilias = get_subfamilias(db)
    return subfamilias


@insumo.get("/insumo/rubro_insumos/", response_model=list[RubroInsumo], tags=['INSUMO'])
def read_rubro_insumos(db: Session = Depends(get_db)):
    rubro_insumos = get_rubro_insumos(db)
    return rubro_insumos


@insumo.get("/insumo/tipo_erogaciones/", response_model=list[TipoErogacion], tags=['INSUMO'])
def read_tipo_erogaciones(db: Session = Depends(get_db)):
    tipo_erogaciones = get_tipo_erogaciones(db)
    return tipo_erogaciones


@insumo.get("/insumo/tipo_movimiento_insumos/", response_model=list[TipoMovimientoInsumo], tags=['INSUMO'])
def read_tipo_movimiento_insumos(db: Session = Depends(get_db)):
    # return get_movimiento_insumos(db)
    return db.query(Alta_tipo_movimiento_modelo).all()


#################################################((***))######################################################


##############################################################################################################
################################        CRUD INSUMOS       ###################################################
##############################################################################################################


@insumo.get("/insumos/", tags=['INSUMO'])
def read_insumos(
    page_num: Optional[int] = None,
    page_size: Optional[int] = None,
    db: Session = Depends(get_db)
):
    insumos = get_insumos(db=db, page_size=page_size, page_num=page_num)
    
    response = paginate(db=db, data=insumos,
                        tabla="insumos", page_size=page_size)
    return JSONResponse(response, status_code=200)


@insumo.post("/create_insumos/", response_model=Insumo, status_code=status.HTTP_201_CREATED, tags=['INSUMO'])
def post_insumo(insumo: InsumoBase, id_sql_lite: Optional[int] = None, db: Session = Depends(get_db)):
    db_insumo = get_insumo(db, nombre=insumo.nombre)
    if db_insumo:
        raise HTTPException(status_code=400, detail="El insumo ya existe!")

    response_sql = create_insumo(db=db, insumo=insumo)
    # transformo a json
    response_sql = jsonable_encoder(response_sql)
    response = {'id_sql_lite': id_sql_lite, 'id_database': response_sql['id']}
    return JSONResponse(jsonable_encoder(response))


@insumo.put("/update_insumo", tags=['INSUMO'])
def update_insumo(insumo: InsumoBase, id: int, db: Session = Depends(get_db)):
    try:

        # db_insumo = get_insumo(db, nombre=insumo.nombre)
        # if db_insumo:
        #     raise HTTPException(status_code=400, detail="El insumo ya existe!")
        # # if insumo.updated_at is None:
        #     #Si no mandan por defecto el update_at se debe crear
        #     updated_at = datetime.datetime.now()

        db.query(Alta_insumo_modelo).\
            filter(Alta_insumo_modelo.id == id).\
            update({Alta_insumo_modelo.nombre: insumo.nombre,
                    Alta_insumo_modelo.abreviatura: insumo.abreviatura,
                    Alta_insumo_modelo.codigo_externo: insumo.codigo_externo,
                    Alta_insumo_modelo.lote_control: insumo.lote_control,
                    Alta_insumo_modelo.vencimiento_control: insumo.vencimiento_control,
                    Alta_insumo_modelo.reposicion_control: insumo.reposicion_control,
                    Alta_insumo_modelo.reposicion_cantidad: insumo.reposicion_cantidad,
                    Alta_insumo_modelo.reposicion_alerta_email: insumo.reposicion_alerta_email,
                    Alta_insumo_modelo.reposicion_alerta: insumo.reposicion_alerta,
                    Alta_insumo_modelo.tarea_id: insumo.tarea_id,
                    Alta_insumo_modelo.unidad_id: insumo.unidad_id,
                    Alta_insumo_modelo.familia_id: insumo.familia_id,
                    Alta_insumo_modelo.subfamilia_id: insumo.subfamilia_id,
                    Alta_insumo_modelo.rubro_insumo_id: insumo.rubro_insumo_id,
                    Alta_insumo_modelo.tipo_erogacion_id: insumo.tipo_erogacion_id,
                    Alta_insumo_modelo.updated_at: insumo.updated_at
                    })
        db.commit()

        return JSONResponse("Insumo Actualizado exitosamente", 200)
    except Exception as e:
        print(e)
        return JSONResponse("Ocurrió un error", 500)


@insumo.delete("/delete_insumos_desarrollo/", tags=['INSUMO'])
def delete_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
            --sql
            DELETE FROM insumos 
            WHERE id = {id};
            """.format(id=id)
    else:
        statement = """
                --sql
                TRUNCATE TABLE insumos CASCADE;
                """
    db.execute(statement)
    return "Los insumos fueron borrados"


@insumo.delete("/delete_insumos/", tags=['INSUMO'])
def delete_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        db.query(Alta_insumo_modelo).filter_by(id=id).\
            update({Alta_insumo_modelo.deleted_at: datetime.datetime.now()})
        db.commit()
        return JSONResponse({"response": "Insumo eliminado"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse({"response": "Ocurrió un error"}, status_code=500)

#################################################((***))######################################################
