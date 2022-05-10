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
from db.database import engine, get_db, Base  # , SessionLocal

insumo = APIRouter()


@insumo.get("/insumos/", tags=['INSUMO'])
def read_insumos(db: Session = Depends(get_db)):
    insumos = get_insumos(db)
    return JSONResponse(jsonable_encoder(insumos))


@insumo.post("/create_insumos/", response_model=Insumo, status_code=status.HTTP_201_CREATED, tags=['INSUMO'])
def crear_insumo(insumo: InsumoBase, db: Session = Depends(get_db)):
    db_insumo = get_insumo(db, nombre=insumo.nombre)
    if db_insumo:
        raise HTTPException(status_code=400, detail="El insumo ya existe!")
    return create_insumo(db=db, insumo=insumo)


@insumo.delete("/delete_insumos/", tags=['INSUMO'])
def delete_insumos(db: Session = Depends(get_db)):
    drop_insumos(db)
    return "Los insumos fueron borrados"


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


# Se agregó
@insumo.get("/insumo/tipo_movimiento_insumos/", response_model=list[TipoMovimientoInsumo], tags=['INSUMO'])
def read_tipo_movimiento_insumos(db: Session = Depends(get_db)):
    tipo_erogaciones = get_movimiento_insumos(db)
    return tipo_erogaciones


# STOCK ALMACEN/INSUMOS/MOVIMIENTOS
@insumo.get("/stock_almacen_insumos/",  tags=['STOCK'])
def stocks(db: Session = Depends(get_db)):
    return get_stock_almacen(db=db)


@insumo.post("/create_stock_almacen_insumos/", response_model=StockAlmacenInsumo, status_code=status.HTTP_201_CREATED, tags=['STOCK'])
def crear_stock_almacen_insumo(stock: StockAlmacenInsumoBase, db: Session = Depends(get_db)):
    return create_stock_almacen_insumo(db=db, stock=stock)


@insumo.delete("/stock_almacen_insumos/{id}",  tags=['STOCK'])
def delete_stock(id: str, db: Session = Depends(get_db)):
    try:
        db.query(Stock_almacen_insumo_modelo).filter(Stock_almacen_insumo_modelo.id == id).\
            delete(synchronize_session=False)
        db.commit()

        return JSONResponse("Stock eliminado", 200)
    except:
        return JSONResponse("Hubo un error", 500)


@insumo.get("/movimiento_insumo/", tags=['STOCK-MOVIMIENTOS'])
def get_movimiento_insumos(db: Session = Depends(get_db)):
    return db.query(Moviemiento_insumos_modelo).all()


@insumo.post("/create_movimiento_insumos/", response_model=MovimientoInsumo, status_code=status.HTTP_201_CREATED, tags=['STOCK-MOVIMIENTOS'])
def crear_movimiento_insumo(movimiento: MovimientoInsumoBase, db: Session = Depends(get_db)):

    create_movimiento_insumos_almacen(
        db=db,
        cantidad=movimiento.cantidad,
        insumo_id=movimiento.insumo_id,
        id_almacen_origen=movimiento.origen_almacen_id,
        id_almacen_destino=movimiento.destino_almacen_id,
    )

    return create_movimiento_insumo(db=db, movimiento=movimiento)


@insumo.delete("/delete_movimiento_insumo/{id}", tags=['STOCK-MOVIMIENTOS'])
def delete_movimiento_insumo(id: str, db: Session = Depends(get_db)):

    try:

        db.query(Moviemiento_insumos_modelo).filter(Moviemiento_insumos_modelo.id == id).\
            delete(synchronize_session=False)
        db.commit()
        return JSONResponse("Movimiento eliminado", 200)
    except:
        return JSONResponse("Hubo un error", 500)
