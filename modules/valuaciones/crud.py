from ast import In
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from modules.insumo import models, schemas
from modules.valuaciones.schemas import *
from sqlalchemy import update
import datetime
import json
from modules.valuaciones.models import *


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
    cantidad = abs(cantidad)
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
    db: Session,
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

    statement = ""

    if nro_metodo == 1:
        statement = """
                       --sql
                       SELECT * FROM
                       insumos_valorizacion
                       WHERE insumos_valorizacion.insumo_id = {insumo_id}
                       AND insumos_valorizacion.tipo_movimiento_id = 1
                       ORDER BY id DESC;""".format(
            insumo_id=insumo_id,
            tipo_movimiento_id=tipo_movimiento_id
        )

    if nro_metodo == 2:
        statement = """
                       --sql
                       SELECT * FROM
                       insumos_valorizacion
                       WHERE insumos_valorizacion.insumo_id = {insumo_id}
                       AND insumos_valorizacion.tipo_movimiento_id = 1
                       ORDER BY id ASC;""".format(
            insumo_id=insumo_id,
            tipo_movimiento_id=tipo_movimiento_id
        )

    if cantidad < 0:
        # momentaneamente por ajuste la cantidad a restar debe ser negativa
        # por eso se crea este if
        cantidad = abs(cantidad)

        valuaciones = db.execute(statement).all()
        valuaciones = jsonable_encoder(valuaciones)

        """
        de este primer insumo necesito saber cuantas unidades salen
        y reflejar ese valor en la tabla
        de donde saco esas unidades?
        """

        cantidad_final = valuaciones[0]["cantidad"] - cantidad
        #print("cantidad movimiento")
        # print(valuaciones[0]["cantidad"])
        #print("cantidad final:")
        # print(cantidad_final)
        # creo una variable que almacena el precio_unitario final
        precio_unitario_final = 0
        # creo una variable que almacena el precio total final
        precio_total_final = 0

        if cantidad_final < 0:
            # si la cantidad final es menor a cero debo agarrar otra columna y restarle la cantidad a esa
            # debo repetir este proceso hasta que la cantidad final sea 0
            i = 1
            precio_total_final += valuaciones[0]['precio_total']

            db.query(Insumos_valorizacion).\
                filter(Insumos_valorizacion.id == valuaciones[0]['id']).\
                update({Insumos_valorizacion.cantidad: 0,
                        Insumos_valorizacion.precio_total: 0})

            while cantidad_final < 0:

                cantidad_final = valuaciones[i]['cantidad'] - \
                    abs(cantidad_final)
                # actualizar los valores de las tablas con un update
                if cantidad_final < 0:
                    precio_total_final += valuaciones[i]['precio_total']

                    db.query(Insumos_valorizacion).\
                        filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                        update({Insumos_valorizacion.cantidad: 0,
                                Insumos_valorizacion.precio_total: 0})

                else:
                    precio_total_restado = (
                        valuaciones[i]['cantidad'] - cantidad_final) * valuaciones[i]['precio_unitario']
                    print(precio_total_restado)
                    precio_total_final += precio_total_restado
                    print(precio_total_restado)
                    db.query(Insumos_valorizacion).\
                        filter(Insumos_valorizacion.id == valuaciones[i]['id']).\
                        update(
                            {Insumos_valorizacion.cantidad: cantidad_final,
                             Insumos_valorizacion.precio_total: cantidad_final * Insumos_valorizacion.precio_unitario}
                    )

                db.commit()
                precio_unitario_final = valuaciones[i]['precio_unitario']
                i += 1

        else:
            # actualizar el valor de la resta
            db.query(Insumos_valorizacion).\
                filter(Insumos_valorizacion.id == valuaciones[0]['id']).\
                update({Insumos_valorizacion.cantidad: cantidad_final})
            db.commit()

        db_insumo_valorizacion = Insumos_valorizacion(**{
            "cantidad": cantidad,
            "precio_unitario": precio_unitario_final,
            "precio_total": precio_total_final,
            "almacen_id": almacen_id,
            "movimiento": movimiento,
            "tipo_movimiento_id": tipo_movimiento_id,
            "insumo_id": insumo_id
        })
        db.add(db_insumo_valorizacion)
        db.commit()
        db.refresh(db_insumo_valorizacion)
    else:
        return "Por el momento no se admiten otras operaciones"


def administrar_ppp(
    db: Session,
    cantidad: float,
    almacen_id: int,
    movimiento: str,
    tipo_movimiento_id: int,
    insumo_id: int
):

    statement = """
    --sql
    SELECT * FROM 
    insumos_valorizacion 
    WHERE insumos_valorizacion.insumo_id = {insumo_id} 
    AND insumos_valorizacion.tipo_movimiento_id = 1;
    """.format(
        insumo_id=insumo_id
    )
    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)
    if cantidad < 0:
        cantidad = abs(cantidad)
    # si es un ajuste tengo que retirarlo al precio promedio
    # por lo tanto debo sumar  las cantidades anteriores y sacarle el promedio total (precio)
    cantidad_total = 0
    precio_total = 0

    for valuacion in valuaciones:
        cantidad_total += valuacion["cantidad"]
        precio_total += valuacion["precio_total"]

    # precio unitario promedio
    precio_unitario_promedio = precio_total / cantidad_total

    precio_total = precio_unitario_promedio * cantidad
    db_insumo_valorizacion = Insumos_valorizacion(**{
        "cantidad": cantidad,
        "precio_unitario": precio_unitario_promedio,
        "precio_total": precio_total,
        "almacen_id": almacen_id,
        "movimiento": movimiento,
        "tipo_movimiento_id": tipo_movimiento_id,
        "insumo_id": insumo_id
    })
    db.add(db_insumo_valorizacion)
    db.commit()
    db.refresh(db_insumo_valorizacion)
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
    # armar un movimiento que me permita  establecer un percio general por cada insumo
    # en administrar criterio solo te va importar el dato que ingreses y nada mas
    # si no creaste ninguna cotizacion se usa como general el ultimo ingreso
    statement = """
        --sql
        SELECT * FROM 
        insumos_valorizacion 
        WHERE insumo_id = {insumo_id} 
        ORDER BY id DESC;""".format(insumo_id=insumo_id)

    valuaciones = db.execute(statement).all()
    valuaciones = jsonable_encoder(valuaciones)

    # logaritmo armado en caso de necesitar mas de una configuracion
    # configuraciones = jsonable_encoder(configuraciones)
    # configuraciones = configuraciones['configuraciones']
    # configuraciones = json.loads(configuraciones)
    # print(configuraciones)

    # en caso de necesitar una configuracion:
    config = db.query(Tipo_Valorizacion_Empresas).\
        filter(Tipo_Valorizacion_Empresas.empresa_id == 1,
               Tipo_Valorizacion_Empresas.metodo_id == 4
               ).first()
    config = jsonable_encoder(config)

    if config['config'] == True:

        precio_ultimo_ingreso = precio_unitario
        # Establecer un precio general por cada insumo
    else:
        # busco en la tabla de cotizaciones y selecciono la ultima cotizacion ingresada
        historicos = db.query(Historicos_Precio_Segun_Criterio).filter(
            Historicos_Precio_Segun_Criterio.insumo_id == insumo_id
        )
        historicos = jsonable_encoder(historicos)
        precio_ultimo_ingreso = historicos[len(historicos) - 1]['precio']

    for valuacion in valuaciones:
        # filtro tipo de movimiento_id
        if valuacion["tipo_movimiento_id"] == 1 and valuacion['cantidad'] > 0:
            db.query(Insumos_valorizacion).\
                filter(Insumos_valorizacion.id == valuacion["id"]).\
                update({Insumos_valorizacion.precio_unitario: precio_ultimo_ingreso})

    create_valorizacion(
        db=db,
        cantidad=cantidad,
        precio_unitario=precio_ultimo_ingreso,
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

    metodo_valorizacion = db.query(
        Tipo_Valorizacion_Empresas
    ).filter_by(id=empresa_id).first()

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
            almacen_id=almacen_id,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id,
            movimiento=movimiento,
        )

    elif nro_metodo == 4:

        administrar_precio_segun_criterio(
            db=db,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            almacen_id=almacen_id,
            movimiento=movimiento,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id
        )


def create_cotizacion(db: Session, cotizacion: Cotizacion):
    db_cotizacion = Historicos_Precio_Segun_Criterio(**cotizacion.dict())
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion
