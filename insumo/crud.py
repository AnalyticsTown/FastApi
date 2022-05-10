from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
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
                   reposicion_alerta_email, detalle_tarea, detalle_unidad, detalle_familia, detalle_subfamilia, detalle_rubro_insumo, nombre_tipo_erogacion, abreviatura_tipo_erogacion
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


def create_movimiento_insumo(db: Session, movimiento: schemas.MovimientoInsumoBase):  # Se agregó
    db_insumo = models.Moviemiento_insumos_modelo(**movimiento.dict())
    db.add(db_insumo)
    db.commit()
    db.refresh(db_insumo)
    return db_insumo


def create_stock_almacen_insumo(db: Session, stock: schemas.StockAlmacenInsumoBase):  # Se agregó
    db_insumo = models.Stock_almacen_insumo_modelo(**stock.dict())
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


def create_movimiento_insumos_almacen(db: Session, cantidad: float, insumo_id: int, id_almacen_origen: int, id_almacen_destino: int):
    # actualizamos las cantidades de insumos de los almacenes

    insumo_en_almacen_destino = db.query(models.Stock_almacen_insumo_modelo).\
        filter(
            models.Stock_almacen_insumo_modelo.insumo_id == insumo_id,
            models.Stock_almacen_insumo_modelo.almacen_id == id_almacen_destino
    )

    if insumo_en_almacen_destino:
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
        # Añado el insumo en el almacen

        insumo_stock = {
            "cantidad": cantidad,
            "insumo_id": insumo_id,
            "almacen_id": id_almacen_destino
        }

        create_stock_almacen_insumo(db=db, stock=insumo_stock)
