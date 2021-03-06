from typing import Optional
from sqlalchemy.orm import Session
from modules.helpers.pagination import pagination_sql
from modules.insumo import models, schemas
from modules.valuaciones.models import *

##############################################################################################################
########################################  STOCKS   ###########################################################
##############################################################################################################


def get_stock_almacen(db: Session):
    statement = """
                --sql
                SELECT * FROM stocks
                LEFT JOIN insumos ON insumos.id = stocks.insumo_id
                LEFT JOIN almacenes ON almacenes.id = stocks.almacen_id;
                """
    return db.execute(statement).all()


def create_stock_almacen_insumo(db: Session, stock: schemas.StockAlmacenInsumoBase):  # Se agregó
    db_insumo = models.Stock_almacen_insumo_modelo(**stock)
    db.add(db_insumo)
    db.commit()
    db.refresh(db_insumo)
    return db_insumo


################################################################################################
################################### DETALLE MOVIMIENTO #########################################
################################################################################################


def create_movimiento_detalle(db: Session, movimiento: schemas.MovimientoDetalle):  # Se agregó
    db_movimiento = models.Movimiento_detalle_modelo(**movimiento)
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def get_movimiento_detalle(
    db: Session, 
    id: Optional[int],
    page_size: Optional[int] = None, 
    page_num: Optional[int] = None 
):
    text = pagination_sql(page_num=page_num, page_size=page_size)
    
    if id:
        
        statement = """
                --sql
                SELECT
                movimiento_detalle.id,
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                movimiento_detalle.precio_total,
                abr AS unidad,
                em.nro_movimiento,
                em.fecha_valor,
                almacenes.nombre AS almacen_origen,
                a.nombre AS almacen_destino,
                t.detalle_tipo_movimiento_insumo AS movimiento,
                i.nombre AS insumo
                FROM movimiento_detalle
                LEFT JOIN encabezado_movimiento AS em ON em.id = movimiento_detalle.encabezado_movimiento_id
                LEFT JOIN tipo_movimiento_insumos AS t ON t.id = em.tipo_movimiento_id
                LEFT JOIN almacenes AS a ON a.id = em.destino_almacen_id
                LEFT JOIN almacenes ON almacenes.id = em.origen_almacen_id
                LEFT JOIN unidades AS u ON u.id = movimiento_detalle.unidad_id
                LEFT JOIN insumos AS i ON i.id = movimiento_detalle.insumo_id
                WHERE movimiento_detalle.encabezado_movimiento_id = {id};        
            """.format(id=id)
    else:
        
        statement = """
                --sql
                SELECT
                movimiento_detalle.id,
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                movimiento_detalle.precio_total,
                abr AS unidad,
                em.nro_movimiento,
                em.fecha_valor,
                almacenes.nombre AS almacen_origen,
                a.nombre AS almacen_destino,
                t.detalle_tipo_movimiento_insumo AS movimiento,
                i.nombre AS insumo
                FROM movimiento_detalle
                LEFT JOIN encabezado_movimiento AS em ON em.id = movimiento_detalle.encabezado_movimiento_id
                LEFT JOIN tipo_movimiento_insumos AS t ON t.id = em.tipo_movimiento_id
                LEFT JOIN almacenes AS a ON a.id = em.destino_almacen_id
                LEFT JOIN almacenes ON almacenes.id = em.origen_almacen_id
                LEFT JOIN unidades AS u ON u.id = movimiento_detalle.unidad_id
                LEFT JOIN insumos AS i ON i.id = movimiento_detalle.insumo_id
                {text};
                """.format(text=text)
    
    return db.execute(statement).all()


# falta update y delete


################################################################################################
################################ ENCABEZADO MOVIMIENTO #########################################
################################################################################################

def create_encabezado_movimiento(db: Session, encabezado: schemas.EncabezadoInsumos):
    db_encabezado = models.Encabezado_insumos_modelo(**encabezado.dict())
    db.add(db_encabezado)
    db.commit()
    db.refresh(db_encabezado)
    print(db_encabezado)
    return db_encabezado


def get_movimiento_encabezado(db: Session, page_size: int, page_num: int):
    
    if page_size and page_num:
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
                LEFT JOIN tipo_movimiento_insumos ON tipo_movimiento_insumos.id = encabezado_movimiento.tipo_movimiento_id                    
                LIMIT {page_size}
                OFFSET ({page_num} - 1) * {page_size}        
                ORDER BY encabezado_movimiento.created_at;
                """.format(page_size=page_size, page_num=page_num)

    else:
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
                LEFT JOIN tipo_movimiento_insumos ON tipo_movimiento_insumos.id = encabezado_movimiento.tipo_movimiento_id                    
                ORDER BY encabezado_movimiento.created_at;
                """

    return db.execute(statement).all()
