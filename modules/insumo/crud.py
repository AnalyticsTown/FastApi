from typing import Optional
from fastapi.encoders import jsonable_encoder
from graphene import DateTime
from sqlalchemy.orm import Session
from insumo import models, schemas
from valuaciones.models import *

####################################################################################################
################################ DATOS DE INSUMOS DE SOLO LECTURA ##################################
####################################################################################################


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

####################################################################################################
################################ CRUD INSUMOS   ####################################################
####################################################################################################


def get_insumos(db: Session, page_size: int, page_num: int, fecha: Optional[DateTime] = None):

    # compruebo si esta
    if fecha is not None:

        date = "AND created_at > {fecha}".format(fecha=fecha)

    else:

        date = " "

    if page_size and page_num:

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
                    LEFT JOIN tipo_erogaciones ON tipo_erogaciones.id = insumos.tipo_erogacion_id
                    WHERE insumos.deleted_at IS NULL
                    {date}
                    ORDER BY insumos.created_at
                    LIMIT {page_size}
                    OFFSET ({page_num} - 1) * {page_size};
                    """.format(page_size=page_size, page_num=page_num, date=date)

    else:

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
                    LEFT JOIN tipo_erogaciones ON tipo_erogaciones.id = insumos.tipo_erogacion_id
                    WHERE insumos.deleted_at IS NULL
                    {date}
                    ORDER BY insumos.created_at;""".format(date=date)

    response = db.execute(statement).all()
    return jsonable_encoder(response)


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
