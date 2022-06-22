from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
from valuaciones.crud import administrar_precio_segun_criterio, create_valorizacion, ejecutar_metodo_valorizacion
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


def get_insumos(db: Session):
    statement = """
                   --sql
                   SELECT 
                   insumos.id, 
                   activo, 
                   nombre, 
                   abreviatura, 
                   codigo_externo, 
                   lote_control, 
                   vencimiento_control, 
                   reposicion_control, 
                   reposicion_cantidad, 
                   reposicion_alerta,
                   reposicion_alerta_email, 
                   detalle_tarea, 
                   abr, 
                   detalle_familia, 
                   detalle_subfamilia, 
                   detalle_rubro_insumo, 
                   nombre_tipo_erogacion, 
                   abreviatura_tipo_erogacion
                   FROM insumos
                   LEFT JOIN tareas ON insumos.tarea_id = tareas.id
                   LEFT JOIN unidades ON unidades.id = insumos.unidad_id
                   LEFT JOIN familias ON familias.id = insumos.familia_id
                   LEFT JOIN subfamilias ON subfamilias.id = insumos.subfamilia_id
                   LEFT JOIN rubro_insumos ON rubro_insumos.id = insumos.rubro_insumo_id
                   LEFT JOIN tipo_erogaciones ON tipo_erogaciones.id = insumos.tipo_erogacion_id;
                """

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
                --sql
                SELECT * FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id;
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
    nro_movimiento: str,
    tipo_movimiento_id: int
):
    # compruebo si hay stock del insumo con nro_lote y fecha de vencimiento
    if fecha_vencimiento is not None and nro_lote is not None:
        # busco si ese insumo esta presente en la tabla de existencias
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

        # si ya esta el insumo en existencias lo busco y lo actualizo
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
        #si la cantidad del ajuste es negativa se va a restar
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


def get_movimiento_encabezado(db: Session):

    statement = """
            --sql
            SELECT 
            encabezado_movimiento.id,
            detalle_tipo_movimiento_insumo,
            fecha_real,
            fecha_valor,
            nro_movimiento,
            origen_almacen_id,
            destino_almacen_id,
            orden_de_compra,
            almacenes.nombre AS nombre_almacen_origen,
            a.nombre AS almacen_destino,
            detalle_tipo_movimiento_insumo
            FROM encabezado_movimiento
            LEFT JOIN almacenes ON almacenes.id = encabezado_movimiento.origen_almacen_id 
            LEFT JOIN almacenes AS a  ON a.id = encabezado_movimiento.destino_almacen_id
            LEFT JOIN tipo_movimiento_insumos ON tipo_movimiento_insumos.id = encabezado_movimiento.tipo_movimiento_id;        
            """
    return db.execute(statement).all()
