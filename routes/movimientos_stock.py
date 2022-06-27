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
from db.database import engine, get_db, Base  # , SessionLocal
from valuaciones.crud import *

movimiento = APIRouter()
##############################################################################################################
################################  MOVIMIENTOS ENCABEZADO Y DETALLE   #########################################
##############################################################################################################


###################################    ENCABEZADO CRUD    ####################################################

@movimiento.get("/encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def get_encabezado_movimiento(db: Session = Depends(get_db)):
    return get_movimiento_encabezado(db=db)


@movimiento.post("/create_encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def create_encabezado(encabezado: EncabezadoInsumos, db: Session = Depends(get_db)):

    return create_encabezado_movimiento(db=db, encabezado=encabezado)


@movimiento.delete('/encabezado_movimiento/', tags=['ENCABEZADO MOVIMIENTO'])
def borrar_encabezados(db: Session = Depends(get_db)):
    statement = """
        --sql
        TRUNCATE TABLE encabezado_movimiento CASCADE;
        """
    db.execute(statement)
    db.commit()
    return "encabezados eliminados"


###################################    DETALLE  CRUD    ####################################################

@movimiento.get('/movimiento_detalle/', tags=['DETALLE-MOVIMIENTO'])
def movimiento_detalle(id: Optional[str] = None, db: Session = Depends(get_db)):

    statement = """
                --sql
                SELECT
                movimiento_detalle.id,
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                movimiento_detalle.precio_total,
                abr AS unidad,
                em.nro_movimiento,
                em.fecha_valor,
                almacenes.nombre AS almacen_origen,
                a.nombre AS almacen_destino,
                t.detalle_tipo_movimiento_insumo AS movimiento,
                i.nombre AS insumo
                FROM movimiento_detalle
                LEFT JOIN encabezado_movimiento AS em ON em.id = movimiento_detalle.encabezado_movimiento_id
                LEFT JOIN tipo_movimiento_insumos AS t ON t.id = em.tipo_movimiento_id
                LEFT JOIN almacenes AS a ON a.id = em.destino_almacen_id
                LEFT JOIN almacenes ON almacenes.id = em.origen_almacen_id
                LEFT JOIN unidades AS u ON u.id = movimiento_detalle.unidad_id
                LEFT JOIN insumos AS i ON i.id = movimiento_detalle.insumo_id;
                """

    if id:
        # def filtrar(detalle):
        #     return detalle['encabezado_movimiento_id'] == id

        # detalles = jsonable_encoder(db.execute(statement).all())
        # filtrado = [d for d in detalles if filtrar(d)]

        # return filtrado
        statement = """
                --sql
                SELECT
                movimiento_detalle.id,
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                movimiento_detalle.precio_total,
                abr AS unidad,
                em.nro_movimiento,
                em.fecha_valor,
                almacenes.nombre AS almacen_origen,
                a.nombre AS almacen_destino,
                t.detalle_tipo_movimiento_insumo AS movimiento,
                i.nombre AS insumo
                FROM movimiento_detalle
                LEFT JOIN encabezado_movimiento AS em ON em.id = movimiento_detalle.encabezado_movimiento_id
                LEFT JOIN tipo_movimiento_insumos AS t ON t.id = em.tipo_movimiento_id
                LEFT JOIN almacenes AS a ON a.id = em.destino_almacen_id
                LEFT JOIN almacenes ON almacenes.id = em.origen_almacen_id
                LEFT JOIN unidades AS u ON u.id = movimiento_detalle.unidad_id
                LEFT JOIN insumos AS i ON i.id = movimiento_detalle.insumo_id
                WHERE movimiento_detalle.encabezado_movimiento_id = {id};
        """.format(id=id)
        
        return db.execute(statement).all()
    
    else:
        
        return db.execute(statement).all()


@movimiento.post("/create_movimiento_detalle/",  status_code=status.HTTP_201_CREATED, tags=['DETALLE-MOVIMIENTO'])
def crear_movimiento_insumo(movimiento: MovimientoDetalleBase, db: Session = Depends(get_db)):
    # busco el encabezado y lo encuentro
    encabezado = db.query(Encabezado_insumos_modelo).filter_by(
        id=movimiento.encabezado_movimiento_id).first()
    # transformo la respuesta en un json
    encabezado2 = jsonable_encoder(encabezado)
    # busco el insumo asociado al detalle
    insumo = db.query(Alta_insumo_modelo).filter_by(
        id=movimiento.insumo_id).first()
    insumo = jsonable_encoder(insumo)

    if encabezado2['tipo_movimiento_id'] == 1:
        # si el encabezado es una compra
        create_compra(
            db=db,
            cantidad=movimiento.cantidad,
            insumo_id=movimiento.insumo_id,
            id_almacen_destino=encabezado2['destino_almacen_id'],
            observaciones=movimiento.observaciones,
            unidad_id=insumo["unidad_id"],
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
            precio_unitario=movimiento.precio_unitario,
            precio_total=movimiento.precio_total,
            nro_movimiento=encabezado2["nro_movimiento"],
            tipo_movimiento_id=encabezado2["tipo_movimiento_id"]
        )

    if encabezado2['tipo_movimiento_id'] == 2:
        # si el encabezado es un ajuste
        create_ajuste(
            db=db,
            cantidad=movimiento.cantidad,
            id_almacen_destino=encabezado2['destino_almacen_id'],
            insumo_id=movimiento.insumo_id,
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
            nro_movimiento=encabezado2["nro_movimiento"],
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
    # Despues de enviar los datos necesarios para actualizar stock creo el detalle
    return create_movimiento_detalle(db=db, movimiento={
        "insumo_id": movimiento.insumo_id,
        "cantidad": movimiento.cantidad,
        "unidad_id": insumo['unidad_id'],
        "nro_lote": movimiento.nro_lote,
        "fecha_vencimiento": movimiento.fecha_vencimiento,
        "precio_unitario": movimiento.precio_unitario,
        "precio_total": movimiento.precio_total,
        "observaciones": movimiento.observaciones,
        "encabezado_movimiento_id": movimiento.encabezado_movimiento_id
    })


@movimiento.delete("/delete_movimiento_detalle/{id}", tags=['DETALLE-MOVIMIENTO'])
def delete_movimiento_insumo(id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if id:
            db.query(Movimiento_detalle_modelo).filter(Movimiento_detalle_modelo.id == id).\
                delete(synchronize_session=False)
            db.commit()
        else:
            db.query(Movimiento_detalle_modelo).delete()

        return JSONResponse("Movimiento eliminado", 200)
    except:
        return JSONResponse("Hubo un error", 500)


#################################################((***))######################################################
