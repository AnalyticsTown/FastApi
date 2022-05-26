import json
from sqlalchemy import func
from requests import session
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
    # return get_movimiento_insumos(db)
    return db.query(Alta_tipo_movimiento_modelo).all()

# MOVIMIENTO Y ENCABEZADO


@insumo.get("/encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def get_encabezado_movimiento(db: Session = Depends(get_db)):
    return get_movimiento_encabezado(db=db)


@insumo.post("/create_encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def create_encabezado(encabezado: EncabezadoInsumos, db: Session = Depends(get_db)):

    return create_encabezado_movimiento(db=db, encabezado=encabezado)


#MOVIMIENTO DETALLE
@insumo.get('/movimiento_detalle/', tags=['DETALLE-MOVIMIENTO'])
def movimiento_detalle(id: Optional[str] = None, db: Session = Depends(get_db)):

    statement = """
                select
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                abr as unidad,
                i.nombre as insumo
                from movimiento_detalle
                left join unidades as u on u.id = movimiento_detalle.unidad_id
                left join insumos as i on i.id = movimiento_detalle.insumo_id
                """

    if id:
        def filtrar(detalle):
            return detalle['encabezado_movimiento_id'] == id

        detalles = jsonable_encoder(db.execute(statement).all())
        filtrado = [d for d in detalles if filtrar(d)]

        return filtrado
    else:
        return db.execute(statement).all()


@insumo.post("/create_movimiento_detalle/",  status_code=status.HTTP_201_CREATED, tags=['DETALLE-MOVIMIENTO'])
def crear_movimiento_insumo(movimiento: MovimientoDetalleBase, db: Session = Depends(get_db)):
    #busco el encabezado y lo encuentro
    encabezado = db.query(Encabezado_insumos_modelo).filter_by(
        id=movimiento.encabezado_movimiento_id).first()
    movimiento.nro_lote
    encabezado2 = jsonable_encoder(encabezado)
    insumo = db.query(Alta_insumo_modelo).filter_by(
        id=movimiento.insumo_id).first()
    insumo = jsonable_encoder(insumo)

    if encabezado2['tipo_movimiento_id'] == 1:

        create_compra(
            db=db,
            cantidad=movimiento.cantidad,
            insumo_id=movimiento.insumo_id,
            id_almacen_origen=encabezado2['origen_almacen_id'],
            observaciones=movimiento.observaciones,
            unidad_id=insumo["unidad_id"],
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
            precio_unitario=movimiento.precio_unitario
        )

    if encabezado2['tipo_movimiento_id'] == 2:
        create_ajuste(
            db=db,
            cantidad=movimiento.cantidad,
            id_almacen_origen=encabezado2['origen_almacen_id'],
            insumo_id=movimiento.insumo_id,
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
        )

    if encabezado2['tipo_movimiento_id'] == 3:
        create_traslado(
            db=db,
            observaciones=movimiento.observaciones,
            cantidad=movimiento.cantidad,
            insumo_id=movimiento.insumo_id,
            id_almacen_origen=encabezado2['origen_almacen_id'],
            id_almacen_destino=encabezado2['destino_almacen_id'],
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
        )

    return create_movimiento_detalle(db=db, movimiento={
        "insumo_id": movimiento.insumo_id,
        "cantidad": movimiento.cantidad,
        "unidad_id": insumo['unidad_id'],
        "nro_lote": movimiento.nro_lote,
        "fecha_vencimiento": movimiento.fecha_vencimiento,
        "precio_unitario": movimiento.precio_unitario,
        "observaciones": movimiento.observaciones,
        "encabezado_movimiento_id": movimiento.encabezado_movimiento_id
    })


@insumo.delete("/delete_movimiento_detalle/{id}", tags=['DETALLE-MOVIMIENTO'])
def delete_movimiento_insumo(id: str, db: Session = Depends(get_db)):

    try:

        db.query(Movimiento_detalle_modelo).filter(Movimiento_detalle_modelo.id == id).\
            delete(synchronize_session=False)
        db.commit()
        return JSONResponse("Movimiento eliminado", 200)
    except:
        return JSONResponse("Hubo un error", 500)
#===============================================================================#


@insumo.get("/existencias/", tags=['EXISTENCIAS'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id:

        statement = """
                    select 
                    stock_almacen_insumos.id,
                    insumos.nombre as insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    stock_almacen_insumos.nro_lote,
                    almacenes.nombre as almacen,
                    unidades.abr as unidad,
                    stock_almacen_insumos.detalle as detalle,
                    stock_almacen_insumos.cantidad as cantidad
                    from stock_almacen_insumos
                    left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                    left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                    left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                    where stock_almacen_insumos.almacen_id = {id}
                    """.format(id=id)

        return db.execute(statement).all()
    else:
        statement2 = """
                    select 
                    stock_almacen_insumos.id,
                    insumos.nombre as insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    almacenes.nombre as almacen,
                    unidades.abr as unidad,
                    stock_almacen_insumos.detalle as detalle,
                    stock_almacen_insumos.cantidad as cantidad
                    from stock_almacen_insumos
                    left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                    left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                    left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                    
                    """

        return db.execute(statement2).all()


@insumo.get("/existencias/total/", tags=['EXISTENCIAS'])
def get_existencias_total(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
                select 
                insumos.nombre as insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr as unidad,
                sum(stock_almacen_insumos.cantidad) total
                from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                where stock_almacen_insumos.almacen_id = {id}
                group by insumo, insumos.reposicion_control, insumos.reposicion_cantidad, unidad        
        """.format(id=id)
    else:
        statement = """
                select 
                insumos.nombre as insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr as unidad,
                sum(stock_almacen_insumos.cantidad) total
                from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                group by insumo, insumos.reposicion_control, insumos.reposicion_cantidad, unidad        
        """
    return db.execute(statement).all()



