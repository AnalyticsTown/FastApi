from pydoc import pager
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from modules.insumo import models, schemas
from sqlalchemy import update
from modules.valuaciones.crud import administrar_precio_segun_criterio, create_valorizacion, ejecutar_metodo_valorizacion
from modules.valuaciones.models import *
from modules.stocks.crud import *

####################################################################################################
####################################### TRANSACCIONES DE STOCKS ####################################
####################################################################################################


########################################### COMPRA #################################################


def create_compra(
    db: Session,
    cantidad: float,
    insumo_id: int,
    id_almacen_destino: int,
    observaciones: str,
    unidad_id: int,
    fecha_vencimiento: Optional[str],
    nro_lote: Optional[str],
    precio_unitario: float,
    precio_total: float,
    nro_movimiento: str,
    tipo_movimiento_id: int
):
    # compruebo si hay stock del insumo con nro_lote y fecha de vencimiento
    if fecha_vencimiento is not None and nro_lote is not None:
        # busco si ese insumo esta presente en la tabla de stocks
        nro_lote_en_almacen = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
        ).first()
        # lo transformo a un json
        nro_lote_en_almacen = jsonable_encoder(nro_lote_en_almacen)

        print("nro lote en almacen es:")
        print(nro_lote_en_almacen)

        # si existe ese insumo actualizo su stock
        if nro_lote_en_almacen and nro_lote_en_almacen['nro_lote'] is not None:

            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad:
                        models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })

        else:
            # sino creo un nuevo stock referido a ese insumo con su respectivo nro_lote y fecha de vencimiento
            create_stock_almacen_insumo(db=db, stock={
                "detalle": observaciones,
                "cantidad": cantidad,
                "insumo_id": insumo_id,
                "almacen_id": id_almacen_destino,
                "unidad_id": unidad_id,
                "fecha_vencimiento": fecha_vencimiento,
                "nro_lote": nro_lote,
                "precio_unitario": precio_unitario,
                "precio_total": precio_total,
            })

    # en este else cae en caso de no tener control por nro de lote o fecha_de_vencimiento
    else:
        insumo_en_almacen = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
        )
        insumo_en_almacen = jsonable_encoder(insumo_en_almacen)

        # si ya esta el insumo en stocks lo busco y lo actualizo
        if insumo_en_almacen and insumo_en_almacen['insumo_id'] is not None:
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad:
                        models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })
        else:
            # sino lo creo
            create_stock_almacen_insumo(db=db, stock={
                "detalle": observaciones,
                "cantidad": cantidad,
                "insumo_id": insumo_id,
                "almacen_id": id_almacen_destino,
                "unidad_id": unidad_id,
                "fecha_vencimiento": fecha_vencimiento,
                "nro_lote": nro_lote,
                "precio_unitario": precio_unitario,
                "precio_total": precio_total
            })

    #######################SECCION DE VALUACIONES##############################

    # busco si el metodo es el de precio segun criterio
    # de esta manera voy a poder hacer la valuacion segun ese metodo

    precio_segun_criterio = db.query(Tipo_Valorizacion_Empresas).\
        filter(Tipo_Valorizacion_Empresas.empresa_id == 1,
               Tipo_Valorizacion_Empresas.metodo_id == 4).first()
    precio_segun_criterio = jsonable_encoder(precio_segun_criterio)

    print(precio_segun_criterio)

    if precio_segun_criterio and precio_segun_criterio['config']:
        administrar_precio_segun_criterio(
            db=db,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            almacen_id=id_almacen_destino,
            movimiento=nro_movimiento,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id
        )
    else:
        create_valorizacion(
            db=db,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            almacen_id=id_almacen_destino,
            movimiento=nro_movimiento,
            tipo_movimiento_id=tipo_movimiento_id,
            insumo_id=insumo_id
        )

########################################### AJUSTE #################################################


def create_ajuste(
    db: Session,
    cantidad: float,
    id_almacen_destino: int,
    insumo_id: int,
    nro_lote: Optional[str],
    fecha_vencimiento: Optional[str],
    nro_movimiento: Optional[str]
):

    # compruebo que exista el stock por nro de lote y fecha de vencimiento
    if (fecha_vencimiento is not None) and (nro_lote is not None):
        db.query(models.Stock_almacen_insumo_modelo).filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.nro_lote == nro_lote,
        ).\
            update({
                models.Stock_almacen_insumo_modelo.cantidad:
                    models.Stock_almacen_insumo_modelo.cantidad + cantidad
            })
        # si la cantidad del ajuste es negativa se va a restar
        if cantidad < 0:
            ajuste = db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote,
            ).first()
            ajuste = jsonable_encoder(ajuste)
            print(ajuste)
            ejecutar_metodo_valorizacion(
                db=db,
                cantidad=cantidad,
                precio_unitario=ajuste['precio_unitario'],
                almacen_id=ajuste['almacen_id'],
                movimiento=nro_movimiento,
                tipo_movimiento_id=2,
                insumo_id=insumo_id,
                empresa_id=1
            )

    else:

        if cantidad < 0:
            ajuste = db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id,
            ).first()
            ajuste = jsonable_encoder(ajuste)
            print(ajuste)
            ejecutar_metodo_valorizacion(
                db=db,
                cantidad=cantidad,
                precio_unitario=ajuste['precio_unitario'],
                almacen_id=ajuste['almacen_id'],
                movimiento=nro_movimiento,
                tipo_movimiento_id=2,
                insumo_id=insumo_id,
                empresa_id=1
            )
        db.query(models.Stock_almacen_insumo_modelo).filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
        ).\
            update({
                models.Stock_almacen_insumo_modelo.cantidad:
                    models.Stock_almacen_insumo_modelo.cantidad + cantidad
            })


########################################### TRASLADO #################################################

def create_traslado(
    db: Session,
    cantidad: float,
    insumo_id: int,
    id_almacen_origen: int,
    id_almacen_destino: int,
    observaciones: str,
    nro_lote: Optional[str],
    fecha_vencimiento: Optional[str]

):
    # actualizamos las cantidades de insumos de los almacenes
    if (fecha_vencimiento is not None) and (nro_lote is not None):

        insumo_en_almacen_destino = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
        ).first()

        insumo_en_almacen_destino = jsonable_encoder(insumo_en_almacen_destino)

        if insumo_en_almacen_destino and insumo_en_almacen_destino['almacen_id'] is not None:
            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).\
                update(
                    {
                        models.Stock_almacen_insumo_modelo.cantidad:
                            models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )

            # ALMACEN DESTINO
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad:
                        models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })

        else:

            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).\
                update(
                    {
                        models.Stock_almacen_insumo_modelo.cantidad:
                            models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )
            almacen = db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).first()

            almacen_dict = jsonable_encoder(almacen)
            # Añado el insumo en el almacen

            create_stock_almacen_insumo(db=db, stock={
                "detalle": observaciones,
                "cantidad": cantidad,
                "insumo_id": insumo_id,
                "almacen_id": id_almacen_destino,
                "unidad_id": almacen_dict["unidad_id"],
                "fecha_vencimiento": almacen_dict["fecha_vencimiento"],
                "nro_lote": almacen_dict["nro_lote"],
                "precio_unitario": almacen_dict["precio_unitario"]
            })
    else:

        insumo_en_almacen_destino1 = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
        ).first()
        insumo_en_almacen_destino1 = jsonable_encoder(
            insumo_en_almacen_destino1)
        if insumo_en_almacen_destino1 is not None:
            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id).\
                update(
                    {

                        models.Stock_almacen_insumo_modelo.cantidad:
                            models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )

            # ALMACEN DESTINO
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad:
                        models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })
        else:
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id).\
                update(
                    {

                        models.Stock_almacen_insumo_modelo.cantidad:
                            models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )
            almacen1 = db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id)
            almacen_dict1 = jsonable_encoder(almacen1)
            # Añado el insumo en el almacen

            insumo_stock1 = {
                "detalle": observaciones,
                "cantidad": cantidad,
                "insumo_id": insumo_id,
                "almacen_id": id_almacen_destino,
                "unidad_id": almacen_dict1["unidad_id"],
                "fecha_vencimiento": almacen_dict1["fecha_vencimiento"],
                "nro_lote": almacen_dict1["nro_lote"],
                "precio_unitario": almacen_dict1["precio_unitario"]
            }
            create_stock_almacen_insumo(db=db, stock=insumo_stock1)
