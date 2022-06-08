from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from valuaciones.schemas import *
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
    insumo_id: int,
    nro_metodo: int
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

    if nro_metodo == 1:
        statement = "SELECT * FROM insumos_valorizacion ORDER BY DESC;"
    if nro_metodo == 2:
        statement = "SELECT * FROM insumos_valorizacion ORDER BY ASC;"

    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)

    """
    de este primer insumo necesito saber cuantas unidades salen
    y reflejar ese valor en la tabla
    de donde saco esas unidades?
    """

    if tipo_movimiento_id == 2 and cantidad < 0:
        cantidad = -cantidad
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
                    cantidad_final = valuaciones[i]['cantidad'] - \
                        (-cantidad_final)
                    # actualizar los valores de las tablas con un update
                    if cantidad_final < 0:
                        db.query(Insumos_valorizacion).\
                            filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                            update({Insumos_valorizacion.cantidad: 0})
                    else:
                        db.query(Insumos_valorizacion).\
                            filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                            update(
                                {Insumos_valorizacion.cantidad: cantidad_final})
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

    # si es un traslado tengo que retirarlo al precio promedio
    # por lo tanto debo sumar  las cantidades anteriores y sacarle el promedio total (precio)
    cantidad_total = 0
    precio_total = 0
    for movimiento in valuaciones:
        if movimiento["tipo_movimiento_id"] == 1:

            cantidad_total += movimiento["cantidad"]
            precio_total += movimiento["precio_unitario"]

    # precio unitario promedio
    precio_unitario_promedio = precio_total / cantidad_total

    # por eso en este caso la la creacion de la valorizacion se realiza al final
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


def administrar_precio_segun_criterio(
    db: Session,
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
):
    #armar un movimiento que me permita  establecer un percio general por cada insumo
    #en administrar criterio solo te va importar el dato que ingreses y nada mas 
    create_valorizacion(
        db=db,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        almacen_id=almacen_id,
        movimiento=movimiento,
        tipo_movimiento_id=tipo_movimiento_id,
        insumo_id=insumo_id
    )


def elegir_tipo_valorizacion(db: Session, valuacion_empresa: Metodo_valorizacion_empresa):
    db_valuacion_empresas = Tipo_Valorizacion_Empresas(**valuacion_empresa)
    db.add(db_valuacion_empresas)
    db.commit()
    db.refresh(db_valuacion_empresas)
    return db_valuacion_empresas

# armar un metodo para modificar empresa


def ejecutar_metodo_valorizacion(
    db: Session,
    cantidad: float,
    precio_unitario: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int,
    empresa_id: int
):
    ""
    # si uno quiere estudiar medicina se tiene que romper el ogt
    metodo_valorizacion = db.query(
        Tipo_Valorizacion_Empresas).filter_by(id=empresa_id).fist()
    metodo_valorizacion = jsonable_encoder(metodo_valorizacion)

    nro_metodo = metodo_valorizacion["metodo_id"]
    
    if nro_metodo == 1 or nro_metodo == 2:
            admininistrar_peps_ueps(
                db=db,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                almacen_id=almacen_id,
                movimiento=movimiento,
                tipo_movimiento_id=tipo_movimiento_id,
                insumo_id=insumo_id,
                nro_metodo=nro_metodo
            )
    elif nro_metodo == 3:
        administrar_ppp(
            db=db,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            almacen_id=almacen_id,
            movimiento=movimiento,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id
        )
    elif nro_metodo == 4:
        administrar_precio_segun_criterio(db=db,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            almacen_id=almacen_id,
            movimiento=movimiento,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id
            )