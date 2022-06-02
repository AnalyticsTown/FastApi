from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
import datetime
import json
from valuaciones.models import *


def administrar_metodo_peps(db: Session, cantidad: float):
    """
    PRIMERO EN ENTRAR, PRIMERO EN SALIR
    necesito:
    ver que tipo de movimiento es 
    sacar el ultimo de las filas siempre que sea mayor que cero
    dejar de mostrar dicha fila
    y comenzar a utilizar la siguiente en cuanto a fechas
    """
    
    statement = """SELECT * FROM insumos_valorizacion ORDER BY ID DESC;"""
    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)
    """
    de este primer insumo necesito saber cuantas unidades salen
    y reflejar ese valor en la tabla
    de donde saco esas unidades?
    """
    primer_insumo = valuaciones[0]
    
    cantidad_final = primer_insumo['cantidad'] - cantidad
    if cantidad_final < 0:
        #si la cantidad final es menor a cero debo agarrar otra columna y restarle la cantidad a esa
        #debo repetir este proceso hasta que la cantidad final sea 0
        ""
        
def administrar_metodo_ueps():
    statement = """SELECT * FROM insumos_valorizacion ORDER BY ID ASC LIMIT 1;"""
    return ""

def administrar_metodo_ppp():
    return ""

def create_valorizacion(
    db: Session,
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
):

    #necesito indicar el metodo
    
    precio_total = cantidad * precio_unitario
 
    db_valorizacion = Insumos_valorizacion(**{
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "precio_total": precio_total,
        "almacen_id": almacen_id,
        "movimiento": movimiento,
        "tipo_movimiento_id": tipo_movimiento_id,
        "insumo_id": insumo_id
    })
    db.add(db_valorizacion)
    db.commit()
    db.refresh(db_valorizacion)
    



    
    
