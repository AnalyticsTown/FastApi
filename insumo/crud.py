from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
from valuaciones.crud import create_valorizacion_compra
from valuaciones.models import *
import datetime
import json


def get_tareas(db: Session):
    return db.query(models.Alta_tarea_modelo).all()


def get_unidades(db: Session):
    return db.query(models.Alta_unidad_modelo).all()


def get_familias(db: Session):
    return db.query(models.Alta_familia_modelo).all()


def get_subfamilias(db: Session):
    return db.query(models.Alta_subfamilia_modelo).all()


def get_rubro_insumos(db: Session):
    return db.query(models.Alta_rubro_insumo_modelo).all()


def get_tipo_erogaciones(db: Session):
    return db.query(models.Alta_erogacion_modelo).all()


def get_movimiento_insumos(db: Session):  # Se agregó
    return db.query(models.Alta_tipo_movimiento_modelo).all()

# def get_insumos(db: Session):
#     return db.query(models.Alta_insumo_modelo).all()


def get_insumos(db: Session):
    statement = """select insumos.id, activo, nombre, abreviatura, codigo_externo, lote_control, vencimiento_control, reposicion_control, reposicion_cantidad, reposicion_alerta,
                   reposicion_alerta_email, detalle_tarea, abr, detalle_familia, detalle_subfamilia, detalle_rubro_insumo, nombre_tipo_erogacion, abreviatura_tipo_erogacion
                   from insumos
                   left join tareas on insumos.tarea_id = tareas.id
                   left join unidades on unidades.id = insumos.unidad_id
                   left join familias on familias.id = insumos.familia_id
                   left join subfamilias on subfamilias.id = insumos.subfamilia_id
                   left join rubro_insumos on rubro_insumos.id = insumos.rubro_insumo_id
                   left join tipo_erogaciones on tipo_erogaciones.id = insumos.tipo_erogacion_id"""

    return db.execute(statement).all()


def get_insumo(db: Session, nombre: str):
    return db.query(models.Alta_insumo_modelo).filter(models.Alta_insumo_modelo.nombre == nombre).first()


def drop_insumos(db: Session):
    db.query(models.Alta_insumo_modelo).delete()
    db.commit()


def create_insumo(db: Session, insumo: schemas.InsumoBase):
    db_insumo = models.Alta_insumo_modelo(**insumo.dict())
    db.add(db_insumo)
    db.commit()
    db.refresh(db_insumo)
    return db_insumo


def create_encabezado_movimiento(db: Session, encabezado: schemas.EncabezadoInsumos):
    db_encabezado = models.Encabezado_insumos_modelo(**encabezado.dict())
    db.add(db_encabezado)
    db.commit()
    db.refresh(db_encabezado)
    print(db_encabezado)
    return db_encabezado


def create_movimiento_detalle(db: Session, movimiento: schemas.MovimientoDetalle):  # Se agregó
    db_movimiento = models.Movimiento_detalle_modelo(**movimiento)
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def create_stock_almacen_insumo(db: Session, stock: schemas.StockAlmacenInsumoBase):  # Se agregó
    db_insumo = models.Stock_almacen_insumo_modelo(**stock)
    db.add(db_insumo)
    db.commit()
    db.refresh(db_insumo)
    return db_insumo


def get_stock_almacen(db: Session):
    statement = """
                select * from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                """
    return db.execute(statement).all()


# FUNCIONES QUE MODIFICAN LOS STOCKS (EXISTENCIAS)
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
):

    if fecha_vencimiento and nro_lote:
        nro_lote_en_almacen = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
        ).first()
        if nro_lote_en_almacen:
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })
        else:
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
    else:
        insumo_en_almacen = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
        )
        if insumo_en_almacen:
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })
        else:
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
    # create_valorizacion_compra(
    #     db=db,
    #     cantidad=cantidad,
    #     precio_unitario=precio_unitario,
    #     movimiento_entrada=,
    #     almacen_id=id_almacen_destino
    # )


def create_ajuste(
    db: Session,
    cantidad: float,
    id_almacen_destino: int,
    insumo_id: int,
    nro_lote: Optional[str],
    fecha_vencimiento: Optional[str]
):

    if fecha_vencimiento and nro_lote:
        db.query(models.Stock_almacen_insumo_modelo).filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.nro_lote == nro_lote,
        ).\
            update({
                models.Stock_almacen_insumo_modelo.cantidad:  models.Stock_almacen_insumo_modelo.cantidad + cantidad
            })
    else:
        db.query(models.Stock_almacen_insumo_modelo).filter(
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
            models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
        ).\
            update({
                models.Stock_almacen_insumo_modelo.cantidad:  models.Stock_almacen_insumo_modelo.cantidad + cantidad
            })


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
    if fecha_vencimiento and nro_lote:
        insumo_en_almacen_destino = db.query(models.Stock_almacen_insumo_modelo).\
            filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
        ).first()

        if insumo_en_almacen_destino:
            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).\
                update(
                    {
                        models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )

            # ALMACEN DESTINO
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })

        else:

            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).\
                update(
                    {
                        models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )
            almacen = db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.nro_lote == nro_lote).first()

            almacen_dict = jsonable_encoder(almacen)
            # Añado el insumo en el almacen
            print(almacen_dict)

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

        if insumo_en_almacen_destino1:
            # ALMACEN ORIGEN
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id).\
                update(
                    {

                        models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad - cantidad
                    }
            )

            # ALMACEN DESTINO
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id
            ).\
                update({
                    models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad + cantidad
                })
        else:
            db.query(models.Stock_almacen_insumo_modelo).filter(
                models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_origen,
                models.Stock_almacen_insumo_modelo.insumo_id == insumo_id).\
                update(
                    {

                        models.Stock_almacen_insumo_modelo.cantidad: models.Stock_almacen_insumo_modelo.cantidad - cantidad
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


def get_movimiento_encabezado(db: Session):

    statement = """
            select 
            encabezado_movimiento.id,
            detalle_tipo_movimiento_insumo,
            fecha_real,
            fecha_valor,
            nro_movimiento,
            origen_almacen_id,
            destino_almacen_id,
            orden_de_compra,
            almacenes.nombre as nombre_almacen_origen,
            a.nombre as almacen_destino,
            detalle_tipo_movimiento_insumo
            from encabezado_movimiento
            left join almacenes on almacenes.id = encabezado_movimiento.origen_almacen_id 
            left join almacenes as a  on a.id = encabezado_movimiento.destino_almacen_id
            left join tipo_movimiento_insumos on tipo_movimiento_insumos.id = encabezado_movimiento.tipo_movimiento_id        
            """
    return db.execute(statement).all()
