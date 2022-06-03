from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
import datetime
import json
from valuaciones.models import *


def create_valorizacion(
    db: Session,
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
):

    # necesito indicar el metodo

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


def admininistrar_peps_ueps(
    db: Session,  metodo: str,
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
):
    """
    PRIMERO EN ENTRAR, PRIMERO EN SALIR
    necesito:
    ver que tipo de movimiento es 
    sacar el ultimo de las filas siempre que sea mayor que cero
    dejar de mostrar dicha fila
    y comenzar a utilizar la siguiente en cuanto a fechas
    """
    create_valorizacion(
        db=db,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        almacen_id=almacen_id,
        movimiento=movimiento,
        tipo_movimiento_id=tipo_movimiento_id,
        insumo_id=insumo_id
    )
    statement = ""

    if metodo == "UEPS":
        statement = "SELECT * FROM insumos_valorizacion ORDER BY DESC;"
    if metodo == 'PEPS':
        statement = "SELECT * FROM insumos_valorizacion ORDER BY ASC;"

    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)

    """
    de este primer insumo necesito saber cuantas unidades salen
    y reflejar ese valor en la tabla
    de donde saco esas unidades?
    """
    if tipo_movimiento_id == 3:
        
        cantidad_final = valuaciones[0]["cantidad"] - cantidad

        if cantidad_final < 0:
            # si la cantidad final es menor a cero debo agarrar otra columna y restarle la cantidad a esa
            # debo repetir este proceso hasta que la cantidad final sea 0
            i = 1
            db.query(Insumos_valorizacion).\
                filter(Insumos_valorizacion.id == valuaciones[0]['id']).\
                update({Insumos_valorizacion.cantidad: 0})

            while cantidad_final < 0:
                if valuaciones[0]['tipo_movimiento_id'] == 3:
                    cantidad_final = valuaciones[i]['cantidad'] - (-cantidad_final)
                    # actualizar los valores de las tablas con un update
                    if cantidad_final < 0:
                        db.query(Insumos_valorizacion).\
                            filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                            update({Insumos_valorizacion.cantidad: 0})
                    else:
                        db.query(Insumos_valorizacion).\
                            filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                            update({Insumos_valorizacion.cantidad: cantidad_final})
                i += 1

        else:
            # actualizar el valor de la resta
            db.query(Insumos_valorizacion).\
                filter(Insumos_valorizacion.id == valuaciones[0]['id']).\
                update({Insumos_valorizacion.cantidad: cantidad_final})


def administrar_ppp(
    db: Session, 
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
    ):

    statement = "SELECT * FROM Insumos_valorizacion;"    
    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)

    #si es un traslado tengo que retirarlo al precio promedio
    #por lo tanto debo sumar  las cantidades anteriores y sacarle el promedio total (precio)
    cantidad_total = 0
    precio_total = 0
    for movimiento in valuaciones:
        if movimiento["tipo_movimiento_id"] == 1:
           
           cantidad_total += movimiento["cantidad"]
           precio_total += movimiento["precio_unitario"]
        
    #precio unitario promedio   
    precio_unitario_promedio = precio_total / cantidad_total
    
    #por eso en este caso la la creacion de la valorizacion se realiza al final
    create_valorizacion(
        db=db,
        cantidad=cantidad,
        precio_unitario=precio_unitario_promedio,
        almacen_id=almacen_id,
        movimiento=movimiento,
        tipo_movimiento_id=tipo_movimiento_id,
        insumo_id=insumo_id
    )
# seria lo mejor y lo mas eficiente que cuando un insumo se quede en 0 pasarlo a una tabla valorizacion historicos
