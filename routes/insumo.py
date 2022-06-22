import json
import random
import datetime
from sqlalchemy import func
from requests import session
from empresa.models import Alta_empresa_modelo
from insumo.schemas import *
from insumo.models import *
from insumo.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal
from valuaciones.crud import *
insumo = APIRouter()

##############################################################################################################
################################        CRUD INSUMOS       ###################################################
##############################################################################################################


@insumo.get("/insumos/", tags=['INSUMO'])
def read_insumos(db: Session = Depends(get_db)):
    insumos = get_insumos(db)
    return JSONResponse(jsonable_encoder(insumos))


@insumo.post("/create_insumos/", response_model=Insumo, status_code=status.HTTP_201_CREATED, tags=['INSUMO'])
def post_insumo(insumo: InsumoBase, db: Session = Depends(get_db)):
    db_insumo = get_insumo(db, nombre=insumo.nombre)
    if db_insumo:
        raise HTTPException(status_code=400, detail="El insumo ya existe!")
    return create_insumo(db=db, insumo=insumo)


@insumo.put("/update_insumo", tags=['INSUMO'])
def update_insumo(insumo: InsumoBase, id: int, db: Session = Depends(get_db)):
    try:
        db.query(Alta_insumo_modelo).\
            filter({Alta_insumo_modelo.id == id}).\
            update({Alta_insumo_modelo.nombre: insumo.nombre,
                    Alta_insumo_modelo.abreviatura: insumo.abreviatura,
                    Alta_insumo_modelo.codigo_externo: insumo.codigo_externo,
                    Alta_insumo_modelo.lote_control: insumo.lote_control,
                    Alta_insumo_modelo.vencimiento_control: insumo.vencimiento_control,
                    Alta_insumo_modelo.reposicion_control: insumo.reposicion_control,
                    Alta_insumo_modelo.reposicion_cantidad: insumo.reposicion_cantidad,
                    Alta_insumo_modelo.reposicion_alerta: insumo.reposicion_alerta_email,
                    Alta_insumo_modelo.tarea_id: insumo.tarea_id,
                    Alta_insumo_modelo.unidad_id: insumo.unidad_id,
                    Alta_insumo_modelo.familia_id: insumo.familia_id,
                    Alta_insumo_modelo.subfamilia_id: insumo.subfamilia_id,
                    Alta_insumo_modelo.rubro_insumo_id: insumo.rubro_insumo_id,
                    Alta_insumo_modelo.tipo_erogacion_id: insumo.tipo_erogacion_id
                    })
        db.commit()
        db.refresh()
        return JSONResponse("Insumo Actualizado exitosamente", 200)
    except:
        return JSONResponse("Ocurrió un error", 500)


@insumo.delete("/delete_insumos/", tags=['INSUMO'])
def delete_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
            --sql
            DELETE FROM insumos 
            WHERE id = {id};
            """.format(id=id)
    else:
        statement = """
                --sql
                TRUNCATE TABLE insumos CASCADE;
                """
    db.execute(statement)
    return "Los insumos fueron borrados"

#################################################((***))######################################################


##############################################################################################################
################################  DATOS DE INSUMOS DE SÓLO LECTURA   #########################################
##############################################################################################################

@insumo.get("/insumo/tareas/", response_model=list[Tarea], tags=['INSUMO'])
def read_tareas(db: Session = Depends(get_db)):
    tareas = get_tareas(db)
    return tareas


@insumo.get("/insumo/unidades/", response_model=list[Unidad], tags=['INSUMO'])
def read_unidades(db: Session = Depends(get_db)):
    unidades = get_unidades(db)
    return unidades


@insumo.get("/insumo/familias/", response_model=list[Familia], tags=['INSUMO'])
def read_familias(db: Session = Depends(get_db)):
    familias = get_familias(db)
    return familias


@insumo.get("/insumo/subfamilias/", response_model=list[Subfamilia], tags=['INSUMO'])
def read_subfamilias(db: Session = Depends(get_db)):
    subfamilias = get_subfamilias(db)
    return subfamilias


@insumo.get("/insumo/rubro_insumos/", response_model=list[RubroInsumo], tags=['INSUMO'])
def read_rubro_insumos(db: Session = Depends(get_db)):
    rubro_insumos = get_rubro_insumos(db)
    return rubro_insumos


@insumo.get("/insumo/tipo_erogaciones/", response_model=list[TipoErogacion], tags=['INSUMO'])
def read_tipo_erogaciones(db: Session = Depends(get_db)):
    tipo_erogaciones = get_tipo_erogaciones(db)
    return tipo_erogaciones



@insumo.get("/insumo/tipo_movimiento_insumos/", response_model=list[TipoMovimientoInsumo], tags=['INSUMO'])
def read_tipo_movimiento_insumos(db: Session = Depends(get_db)):
    # return get_movimiento_insumos(db)
    return db.query(Alta_tipo_movimiento_modelo).all()


#################################################((***))######################################################

##############################################################################################################
################################  MOVIMIENTOS ENCABEZADO Y DETALLE   #########################################
##############################################################################################################


###################################    ENCABEZADO CRUD    ####################################################

@insumo.get("/encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def get_encabezado_movimiento(db: Session = Depends(get_db)):
    return get_movimiento_encabezado(db=db)


@insumo.post("/create_encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def create_encabezado(encabezado: EncabezadoInsumos, db: Session = Depends(get_db)):

    return create_encabezado_movimiento(db=db, encabezado=encabezado)


@insumo.delete('/encabezado_movimiento/', tags=['ENCABEZADO MOVIMIENTO'])
def borrar_encabezados(db: Session = Depends(get_db)):
    statement = """
        --sql
        TRUNCATE TABLE encabezado_movimiento CASCADE;
        """
    db.execute(statement)
    db.commit()
    return "encabezados eliminados"


###################################    DETALLE  CRUD    ####################################################

@insumo.get('/movimiento_detalle/', tags=['DETALLE-MOVIMIENTO'])
def movimiento_detalle(id: Optional[str] = None, db: Session = Depends(get_db)):

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
                LEFT JOIN insumos AS i ON i.id = movimiento_detalle.insumo_id;
                """

    if id:
        def filtrar(detalle):
            return detalle['encabezado_movimiento_id'] == id

        detalles = jsonable_encoder(db.execute(statement).all())
        filtrado = [d for d in detalles if filtrar(d)]

        return filtrado
    else:
        return db.execute(statement).all()


@insumo.post("/create_movimiento_detalle/",  status_code=status.HTTP_201_CREATED, tags=['DETALLE-MOVIMIENTO'])
def crear_movimiento_insumo(movimiento: MovimientoDetalleBase, db: Session = Depends(get_db)):
    # busco el encabezado y lo encuentro
    encabezado = db.query(Encabezado_insumos_modelo).filter_by(
        id=movimiento.encabezado_movimiento_id).first()
    #transformo la respuesta en un json
    encabezado2 = jsonable_encoder(encabezado)
    #busco el insumo asociado al detalle
    insumo = db.query(Alta_insumo_modelo).filter_by(
        id=movimiento.insumo_id).first()
    insumo = jsonable_encoder(insumo)

    if encabezado2['tipo_movimiento_id'] == 1:
        
        create_compra(
            db=db,
            cantidad=movimiento.cantidad,
            insumo_id=movimiento.insumo_id,
            id_almacen_destino=encabezado2['destino_almacen_id'],
            observaciones=movimiento.observaciones,
            unidad_id=insumo["unidad_id"],
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
            precio_unitario=movimiento.precio_unitario,
            precio_total=movimiento.precio_total,
            nro_movimiento=encabezado2["nro_movimiento"],
            tipo_movimiento_id=encabezado2["tipo_movimiento_id"]
        )

    if encabezado2['tipo_movimiento_id'] == 2:
        create_ajuste(
            db=db,
            cantidad=movimiento.cantidad,
            id_almacen_destino=encabezado2['destino_almacen_id'],
            insumo_id=movimiento.insumo_id,
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
            nro_movimiento=encabezado2["nro_movimiento"],
        )

    if encabezado2['tipo_movimiento_id'] == 3:
        create_traslado(
            db=db,
            observaciones=movimiento.observaciones,
            cantidad=movimiento.cantidad,
            insumo_id=movimiento.insumo_id,
            id_almacen_origen=encabezado2['origen_almacen_id'],
            id_almacen_destino=encabezado2['destino_almacen_id'],
            fecha_vencimiento=movimiento.fecha_vencimiento,
            nro_lote=movimiento.nro_lote,
        )

    return create_movimiento_detalle(db=db, movimiento={
        "insumo_id": movimiento.insumo_id,
        "cantidad": movimiento.cantidad,
        "unidad_id": insumo['unidad_id'],
        "nro_lote": movimiento.nro_lote,
        "fecha_vencimiento": movimiento.fecha_vencimiento,
        "precio_unitario": movimiento.precio_unitario,
        "precio_total": movimiento.precio_total,
        "observaciones": movimiento.observaciones,
        "encabezado_movimiento_id": movimiento.encabezado_movimiento_id
    })


@insumo.delete("/delete_movimiento_detalle/{id}", tags=['DETALLE-MOVIMIENTO'])
def delete_movimiento_insumo(id: Optional[str] = None, db: Session = Depends(get_db)):

    try:
        if id:
            db.query(Movimiento_detalle_modelo).filter(Movimiento_detalle_modelo.id == id).\
                delete(synchronize_session=False)
            db.commit()
        else:
            db.query(Movimiento_detalle_modelo).delete()

        return JSONResponse("Movimiento eliminado", 200)
    except:
        return JSONResponse("Hubo un error", 500)


#################################################((***))######################################################

##############################################################################################################
################################          EXISTENCIAS (STOCKS)       #########################################
##############################################################################################################

@insumo.get("/existencias/", tags=['EXISTENCIAS'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id:

        statement = """
                    --sql
                    SELECT 
                    stock_almacen_insumos.id,
                    insumos.nombre AS insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    stock_almacen_insumos.nro_lote,
                    almacenes.nombre AS almacen,
                    unidades.abr AS unidad,
                    stock_almacen_insumos.detalle AS detalle,
                    stock_almacen_insumos.cantidad AS cantidad
                    FROM stock_almacen_insumos
                    LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                    LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                    LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                    WHERE stock_almacen_insumos.almacen_id = {id};
                    """.format(id=id)

    else:
        statement = """
                    --sql
                    SELECT 
                    stock_almacen_insumos.id,
                    insumos.nombre AS insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    almacenes.nombre AS almacen,
                    unidades.abr AS unidad,
                    stock_almacen_insumos.detalle AS detalle,
                    stock_almacen_insumos.cantidad AS cantidad
                    FROM stock_almacen_insumos
                    LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                    LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                    LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id;
                    """

    return db.execute(statement).all()


@insumo.get("/existencias/total/", tags=['EXISTENCIAS'])
def get_existencias_total(id: Optional[int] = None, total: Optional[bool] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
                --sql
                SELECT 
                stock_almacen_insumos.precio_total,
                almacenes.nombre,
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                stock_almacen_insumos.fecha_vencimiento,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                WHERE stock_almacen_insumos.almacen_id = {id}
                GROUP BY insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad, 
                almacenes.nombre, 
                stock_almacen_insumos.precio_total, 
                stock_almacen_insumos.fecha_vencimiento;       
        """.format(id=id)

    elif total == True:

        statement = """
                --sql
                SELECT 
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                GROUP BY 
                insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad;
        """

    else:

        statement = """
                --sql    
                SELECT 
                almacenes.nombre,
                insumos.nombre AS insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr AS unidad,
                SUM(stock_almacen_insumos.cantidad) total
                FROM stock_almacen_insumos
                LEFT JOIN insumos ON insumos.id = stock_almacen_insumos.insumo_id
                LEFT JOIN unidades ON unidades.id = stock_almacen_insumos.unidad_id
                LEFT JOIN almacenes ON almacenes.id = stock_almacen_insumos.almacen_id
                GROUP BY 
                insumo, 
                insumos.reposicion_control, 
                insumos.reposicion_cantidad, 
                unidad, 
                almacenes.nombre;
            """
    return db.execute(statement).all()


@insumo.delete('/existencias/', tags=['EXISTENCIAS'])
def borrar_existencias(db: Session = Depends(get_db)):
    db.query(Stock_almacen_insumo_modelo).delete()
    db.commit()
    return "Existencia eliminadas"


##############################################################################################################
################################          VALUACIONES DE INSUMOS     #########################################
##############################################################################################################


@insumo.get('/metodos_valuacion/', tags=["VALUACIÓN"])
def get_metodos_valorizacion(db: Session = Depends(get_db)):
    return db.query(Tipo_Metodo_Valorizacion).all()


@insumo.get('/ver_metodos_valuacion_empresas/', tags=["VALUACIÓN"])
def get_ver_metodos_valorizacion(db: Session = Depends(get_db)):
    return db.query(Tipo_Valorizacion_Empresas).all()


@insumo.post('/elegir_metodo_valuacion/', tags=["VALUACIÓN"])
def elegir_metodo_valuacion(empresa_id: int, metodo_id: int, config: Optional[bool] = None, db: Session = Depends(get_db)):
    metodo_valuacion = db.query(Tipo_Valorizacion_Empresas).filter(
        Tipo_Valorizacion_Empresas.empresa_id == empresa_id).first()
    metodo_valuacion = jsonable_encoder(metodo_valuacion)

    print(metodo_valuacion)

    if metodo_valuacion and metodo_valuacion['metodo_id'] == 4:
        statement = """
            --sql
            UPDATE tipo_valorizacion_empresas SET 
            metodo_id = {metodo_id},
            config = {config}
            WHERE id = {empresa_id};
        """.format(metodo_id=metodo_id, empresa_id=empresa_id, config=config)

        db.execute(statement)
        db.commit()
        return "Modificion exitosa"
    if metodo_valuacion:
        statement = """
            --sql
            UPDATE tipo_valorizacion_empresas 
            SET metodo_id = {metodo_id} 
            WHERE id = {empresa_id};
        """.format(metodo_id=metodo_id, empresa_id=empresa_id)
        print(statement)
        db.execute(statement)
        db.commit()
        return "Modificion exitosa"
    else:
        return elegir_tipo_valorizacion(
            db=db,
            valuacion_empresa={
                "empresa_id": empresa_id, "metodo_id": metodo_id}
        )


@insumo.get('/mostrar_valorizacion_entradas/', tags=["VALUACIÓN"])
def mostrar_valorizacin(insumo_id: int, db: Session = Depends(get_db)):
    statement = """
            --sql
            SELECT 
            insumos_valorizacion.id,
            insumos_valorizacion.cantidad,
            insumos_valorizacion.precio_unitario,
            insumos_valorizacion.precio_total,
            almacenes.nombre AS almacen,
            insumos_valorizacion.movimiento,
            tipo_movimiento_insumos.detalle_tipo_movimiento_insumo AS tipo_movimiento,
            insumos.nombre AS insumo
            FROM insumos_valorizacion 
            LEFT JOIN almacenes ON almacenes.id = insumos_valorizacion.almacen_id 
            LEFT JOIN insumos ON insumos.id = insumos_valorizacion.insumo_id
            LEFT JOIN tipo_movimiento_insumos ON tipo_movimiento_insumos.id = insumos_valorizacion.tipo_movimiento_id
            WHERE insumos_valorizacion.tipo_movimiento_id = 1
            AND insumos_valorizacion.insumo_id = {insumo_id}
            AND insumos_valorizacion.cantidad > 0;
    """.format(insumo_id=insumo_id)
    return db.execute(statement).all()


@insumo.get('/mostrar_valorizacion_salidas/', tags=["VALUACIÓN"])
def mostrar_valorizacin(insumo_id: int, db: Session = Depends(get_db)):

    statement = """
            --sql
            SELECT 
            insumos_valorizacion.id,
            insumos_valorizacion.cantidad,
            insumos_valorizacion.precio_unitario,
            insumos_valorizacion.precio_total,
            almacenes.nombre AS almacen,
            insumos_valorizacion.movimiento,
            tipo_movimiento_insumos.detalle_tipo_movimiento_insumo AS tipo_movimiento,
            insumos.nombre AS insumo
            FROM insumos_valorizacion 
            LEFT JOIN almacenes ON almacenes.id = insumos_valorizacion.almacen_id 
            LEFT JOIN insumos ON insumos.id = insumos_valorizacion.insumo_id
            LEFT JOIN tipo_movimiento_insumos ON tipo_movimiento_insumos.id = insumos_valorizacion.tipo_movimiento_id
            WHERE 
            insumos_valorizacion.insumo_id = {insumo_id}
            AND insumos_valorizacion.tipo_movimiento_id = 2;
    """.format(insumo_id=insumo_id)
    return db.execute(statement).all()


@insumo.get('/mostrar_valorizacion_saldo/', tags=["VALUACIÓN"])
def mostrar_valorizacion_total(insumo_id: int, db: Session = Depends(get_db)):
    statement1 = """
                --sql
                SELECT
                i.nombre AS insumo,
                SUM(insumos_valorizacion.precio_total) AS precio_total,  
                SUM(insumos_valorizacion.cantidad) cantidad_total
                FROM  insumos_valorizacion
                LEFT JOIN insumos AS i ON i.id = insumos_valorizacion.insumo_id
                WHERE insumo_id = {insumo_id}
                AND cantidad > 0
                AND tipo_movimiento_id = 1
                GROUP BY insumo;
    """.format(insumo_id=insumo_id)
    # armar para ueps peps ppp precio_criterio diferentes consultas
    return db.execute(statement1).all()

###################################    MÉTODO PRECIO SEGÚN CRITERIO   ####################################################


@insumo.post('/ingresar_cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def insumo_cotizacion(cotizacion: Cotizacion, db: Session = Depends(get_db)):

    return create_cotizacion(db=db, cotizacion=cotizacion)


@insumo.get('/cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def get_cotizacion(db: Session = Depends(get_db)):
    # armar el statement para retornar con el nombre
    statement = """
        --sql
        SELECT 
        historicos_precio_segun_criterio.fecha, 
        historicos_precio_segun_criterio.precio,
        insumos.nombre AS insumo 
        FROM 
        historicos_precio_segun_criterio
        LEFT JOIN insumos ON insumos.id = historicos_precio_segun_criterio.insumo_id;
    """
    return db.execute(statement).all()
