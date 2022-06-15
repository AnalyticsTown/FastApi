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


@insumo.get("/insumos/", tags=['INSUMO'])
def read_insumos(db: Session = Depends(get_db)):
    insumos = get_insumos(db)
    return JSONResponse(jsonable_encoder(insumos))


@insumo.post("/create_insumos/", response_model=Insumo, status_code=status.HTTP_201_CREATED, tags=['INSUMO'])
def crear_insumo(insumo: InsumoBase, db: Session = Depends(get_db)):
    db_insumo = get_insumo(db, nombre=insumo.nombre)
    if db_insumo:
        raise HTTPException(status_code=400, detail="El insumo ya existe!")
    return create_insumo(db=db, insumo=insumo)


@insumo.delete("/delete_insumos/", tags=['INSUMO'])
def delete_insumos(db: Session = Depends(get_db)):
    drop_insumos(db)
    return "Los insumos fueron borrados"


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


# Se agregó
@insumo.get("/insumo/tipo_movimiento_insumos/", response_model=list[TipoMovimientoInsumo], tags=['INSUMO'])
def read_tipo_movimiento_insumos(db: Session = Depends(get_db)):
    # return get_movimiento_insumos(db)
    return db.query(Alta_tipo_movimiento_modelo).all()

# MOVIMIENTO Y ENCABEZADO


@insumo.get("/encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def get_encabezado_movimiento(db: Session = Depends(get_db)):
    return get_movimiento_encabezado(db=db)


@insumo.post("/create_encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def create_encabezado(encabezado: EncabezadoInsumos, db: Session = Depends(get_db)):

    return create_encabezado_movimiento(db=db, encabezado=encabezado)


@insumo.delete('/encabezado_movimiento/', tags=['ENCABEZADO MOVIMIENTO'])
def borrar_encabezados(db: Session = Depends(get_db)):
    statement = "truncate table encabezado_movimiento cascade;"
    db.execute(statement)
    db.commit()
    return "encabezados eliminados"
# MOVIMIENTO DETALLE


@insumo.get('/movimiento_detalle/', tags=['DETALLE-MOVIMIENTO'])
def movimiento_detalle(id: Optional[str] = None, db: Session = Depends(get_db)):

    statement = """
                select
                movimiento_detalle.id,
                movimiento_detalle.encabezado_movimiento_id,
                movimiento_detalle.fecha_vencimiento,
                movimiento_detalle.cantidad,
                movimiento_detalle.observaciones,
                movimiento_detalle.nro_lote,
                movimiento_detalle.precio_unitario,
                movimiento_detalle.precio_total,
                abr as unidad,
                em.nro_movimiento,
                em.fecha_valor,
                almacenes.nombre as almacen_origen,
                a.nombre as almacen_destino,
                t.detalle_tipo_movimiento_insumo as movimiento,
                i.nombre as insumo
                from movimiento_detalle
                left join encabezado_movimiento as em on em.id = movimiento_detalle.encabezado_movimiento_id
                left join tipo_movimiento_insumos as t on t.id = em.tipo_movimiento_id
                left join almacenes as a on a.id = em.destino_almacen_id
                left join almacenes on almacenes.id = em.origen_almacen_id
                left join unidades as u on u.id = movimiento_detalle.unidad_id
                left join insumos as i on i.id = movimiento_detalle.insumo_id
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

    encabezado2 = jsonable_encoder(encabezado)
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
#===============================================================================#


@insumo.get("/existencias/", tags=['EXISTENCIAS'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id:

        statement = """
                    select 
                    stock_almacen_insumos.id,
                    insumos.nombre as insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    stock_almacen_insumos.nro_lote,
                    almacenes.nombre as almacen,
                    unidades.abr as unidad,
                    stock_almacen_insumos.detalle as detalle,
                    stock_almacen_insumos.cantidad as cantidad
                    from stock_almacen_insumos
                    left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                    left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                    left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                    where stock_almacen_insumos.almacen_id = {id};
                    """.format(id=id)

        return db.execute(statement).all()
    else:
        statement2 = """
                    
                    select 
                    stock_almacen_insumos.id,
                    insumos.nombre as insumo,
                    insumos.reposicion_alerta,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    stock_almacen_insumos.precio_unitario,
                    stock_almacen_insumos.fecha_vencimiento,
                    almacenes.nombre as almacen,
                    unidades.abr as unidad,
                    stock_almacen_insumos.detalle as detalle,
                    stock_almacen_insumos.cantidad as cantidad
                    from stock_almacen_insumos
                    left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                    left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                    left join unidades on unidades.id = stock_almacen_insumos.unidad_id;
                    """

        return db.execute(statement2).all()


@insumo.get("/existencias/total/", tags=['EXISTENCIAS'])
def get_existencias_total(id: Optional[int] = None, total: Optional[bool] = None, db: Session = Depends(get_db)):
    if id:
        statement = """
                select 
                stock_almacen_insumos.precio_total,
                almacenes.nombre,
                insumos.nombre as insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr as unidad,
                stock_almacen_insumos.fecha_vencimiento,
                sum(stock_almacen_insumos.cantidad) total
                from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                where stock_almacen_insumos.almacen_id = {id}
                group by insumo, insumos.reposicion_control, insumos.reposicion_cantidad, unidad, almacenes.nombre, stock_almacen_insumos.precio_total, stock_almacen_insumos.fecha_vencimiento       
        """.format(id=id)
    elif total == True:
        statement = """
                select 
                insumos.nombre as insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr as unidad,
                sum(stock_almacen_insumos.cantidad) total
                from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                group by insumo, insumos.reposicion_control, insumos.reposicion_cantidad, unidad
        """
    else:

        statement = """
        
                select 
                almacenes.nombre,
                insumos.nombre as insumo,
                insumos.reposicion_control,
                insumos.reposicion_cantidad,
                unidades.abr as unidad,
                sum(stock_almacen_insumos.cantidad) total
                from stock_almacen_insumos
                left join insumos on insumos.id = stock_almacen_insumos.insumo_id
                left join unidades on unidades.id = stock_almacen_insumos.unidad_id
                left join almacenes on almacenes.id = stock_almacen_insumos.almacen_id
                group by insumo, insumos.reposicion_control, insumos.reposicion_cantidad, unidad, almacenes.nombre
            """
    return db.execute(statement).all()


@insumo.delete('/existencias/', tags=['EXISTENCIAS'])
def borrar_existencias(db: Session = Depends(get_db)):
    db.query(Stock_almacen_insumo_modelo).delete()
    db.commit()
    return "Existencia eliminadas"


"""VALORIZACIONES DE INSUMOS"""
# valuaciones de insumos


@insumo.get('/metodos_valorizacion/', tags=["VALORIZACION"])
def get_metodos_valorizacion(db: Session = Depends(get_db)):
    return db.query(Tipo_Metodo_Valorizacion).all()


@insumo.get('/ver_metodos_valorizacion_empresas/', tags=["VALORIZACION"])
def get_ver_metodos_valorizacion(db: Session = Depends(get_db)):
    return db.query(Tipo_Valorizacion_Empresas).all()


@insumo.post('/elegir_metodo_valuacion/', tags=["VALORIZACION"])
def elegir_metodo_valuacion(empresa_id: int, metodo_id: int, config: Optional[bool] = None, db: Session = Depends(get_db)):
    metodo_valuacion = db.query(Tipo_Valorizacion_Empresas).filter(
        Tipo_Valorizacion_Empresas.empresa_id == empresa_id).first()
    metodo_valuacion = jsonable_encoder(metodo_valuacion)

    print(metodo_valuacion)

    if metodo_valuacion['metodo_id'] == 4:
        statement = """
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
            UPDATE tipo_valorizacion_empresas SET metodo_id = {metodo_id} WHERE id = {empresa_id};
        """.format(metodo_id=metodo_id, empresa_id=empresa_id)
        print(statement)
        db.execute(statement)
        db.commit()
        return "Modificion exitosa"
    else:
        return elegir_tipo_valorizacion(db=db, valuacion_empresa={"empresa_id": empresa_id, "metodo_id": metodo_id})


@insumo.get('/mostrar_valorizacion_entradas/', tags=['VALORIZACION'])
def mostrar_valorizacin(insumo_id: int, db: Session = Depends(get_db)):
    statement = """
            select 
            insumos_valorizacion.id,
            insumos_valorizacion.cantidad,
            insumos_valorizacion.precio_unitario,
            insumos_valorizacion.precio_total,
            almacenes.nombre as almacen,
            insumos_valorizacion.movimiento,
            tipo_movimiento_insumos.detalle_tipo_movimiento_insumo as tipo_movimiento,
            insumos.nombre as insumo
            from insumos_valorizacion 
            left join almacenes on almacenes.id = insumos_valorizacion.almacen_id 
            left join insumos on insumos.id = insumos_valorizacion.insumo_id
            left join tipo_movimiento_insumos on tipo_movimiento_insumos.id = insumos_valorizacion.tipo_movimiento_id
            where insumos_valorizacion.tipo_movimiento_id = 1
            and insumos_valorizacion.insumo_id = {insumo_id}
            and insumos_valorizacion.cantidad > 0;
    """.format(insumo_id=insumo_id)
    return db.execute(statement).all()


@insumo.get('/mostrar_valorizacion_salidas/', tags=['VALORIZACION'])
def mostrar_valorizacin(insumo_id: int, db: Session = Depends(get_db)):

    statement = """
            select 
            insumos_valorizacion.id,
            insumos_valorizacion.cantidad,
            insumos_valorizacion.precio_unitario,
            insumos_valorizacion.precio_total,
            almacenes.nombre as almacen,
            insumos_valorizacion.movimiento,
            tipo_movimiento_insumos.detalle_tipo_movimiento_insumo as tipo_movimiento,
            insumos.nombre as insumo
            from insumos_valorizacion 
            left join almacenes on almacenes.id = insumos_valorizacion.almacen_id 
            left join insumos on insumos.id = insumos_valorizacion.insumo_id
            left join tipo_movimiento_insumos on tipo_movimiento_insumos.id = insumos_valorizacion.tipo_movimiento_id
            where 
            insumos_valorizacion.insumo_id = {insumo_id}
            and insumos_valorizacion.tipo_movimiento_id = 2;
    """.format(insumo_id=insumo_id)
    return db.execute(statement).all()


@insumo.get('/mostrar_valorizacion_saldo/', tags=['VALORIZACION'])
def mostrar_valorizacion_total(insumo_id: int, db: Session = Depends(get_db)):
    statement1 = """
                select
                i.nombre as insumo,
                sum(insumos_valorizacion.precio_total) as precio_total,  
                sum(insumos_valorizacion.cantidad) cantidad_total
                from  insumos_valorizacion
                left join insumos as i on i.id = insumos_valorizacion.insumo_id
                where insumo_id = {insumo_id}
                and cantidad > 0
                and tipo_movimiento_id = 1
                group by insumo
    """.format(insumo_id=insumo_id)
    # armar para ueps peps ppp precio_criterio diferentes consultas
    return db.execute(statement1).all()


@insumo.post('/ingresar_cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def insumo_cotizacion(cotizacion: Cotizacion, db: Session = Depends(get_db)):

    return create_cotizacion(db=db, cotizacion=cotizacion)


@insumo.get('/cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def get_cotizacion(db: Session = Depends(get_db)):
    # armar el statement para retornar con el nombre
    statement = """
        select 
        historicos_precio_segun_criterio.fecha, 
        historicos_precio_segun_criterio.precio,
        insumos.nombre as insumo 
        from 
        historicos_precio_segun_criterio
        left join insumos on insumos.id = historicos_precio_segun_criterio.insumo_id
    """
    return db.execute(statement).all()


@insumo.post('/prueba_estres/', tags=['TESTEO BACKEND'])
def ejecutar_prueba_estres(nro_pruebas: int, db: Session = Depends(get_db)):
    # try:
    fecha = datetime.datetime.now()
    insumos_id = [1, 2, 3]
    for n in range(nro_pruebas):
        precio_unitario = random.random() * 100
        cantidad = int(random.random() * 1000)
        db_prueba = models.Stock_almacen_insumo_modelo(**{
            'cantidad': cantidad,
            'detalle': "string",
            'insumo_id': random.choice(insumos_id),
            'almacen_id': 2,
            'nro_lote': 'randomnrolote',
            'fecha_vencimiento': "{dia}/{mes}/{año}".format(dia=fecha.day, mes=fecha.month, año=fecha.year),
            'unidad_id': 1,
            'precio_unitario': precio_unitario,
            'precio_total': precio_unitario * cantidad
        })
        db.add(db_prueba)

    db.commit()
    db.refresh(db_prueba)
    # return JSONResponse("Fake data creada exitosamente")
    # except:
  #  return JSONResponse("Hubo un error", 500)
