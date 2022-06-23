import json
import random
import datetime
from re import A
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

stock = APIRouter()
##############################################################################################################
################################          EXISTENCIAS (STOCKS)       #########################################
##############################################################################################################

@stock.get("/existencias/", tags=['EXISTENCIAS'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id:

        statement = """
                    --sql
                    SELECT 
                    stock_almacen_insumos.id,
                    insumos.nombre AS insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    stock_almacen_insumos.nro_lote,
                    almacenes.nombre AS almacen,
                    unidades.abr AS unidad,
                    stock_almacen_insumos.detalle AS detalle,
                    stock_almacen_insumos.cantidad AS cantidad
                    FROM stock_almacen_insumos
                    LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                    LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                    LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                    WHERE stock_almacen_insumos.almacen_id = {id};
                    """.format(id=id)

    else:
        statement = """
                    --sql
                    SELECT 
                    stock_almacen_insumos.id,
                    insumos.nombre AS insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    almacenes.nombre AS almacen,
                    unidades.abr AS unidad,
                    stock_almacen_insumos.detalle AS detalle,
                    stock_almacen_insumos.cantidad AS cantidad
                    FROM stock_almacen_insumos
                    LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                    LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                    LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id;
                    """

    return db.execute(statement).all()


@stock.get("/existencias/total/", tags=['EXISTENCIAS'])
def get_existencias_total(id: Optional[int] = None, total: Optional[bool] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
                --sql
                SELECT 
                stock_almacen_insumos.precio_total,
                almacenes.nombre,
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                stock_almacen_insumos.fecha_vencimiento,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                WHERE stock_almacen_insumos.almacen_id = {id}
                GROUP BY insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad, 
                almacenes.nombre, 
                stock_almacen_insumos.precio_total, 
                stock_almacen_insumos.fecha_vencimiento;       
        """.format(id=id)

    elif total == True:

        statement = """
                --sql
                SELECT 
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                GROUP BY 
                insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad;
        """

    else:

        statement = """
                --sql    
                SELECT 
                almacenes.nombre,
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                GROUP BY 
                insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad, 
                almacenes.nombre;
            """
    return db.execute(statement).all()


@stock.delete('/existencias/', tags=['EXISTENCIAS'])
def borrar_existencias(db: Session = Depends(get_db)):
    db.query(Stock_almacen_insumo_modelo).delete()
    db.commit()
    return "Existencia eliminadas"


