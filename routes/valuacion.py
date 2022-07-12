import datetime
import random
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modules.insumo.schemas import *
from modules.insumo.models import *
from modules.insumo.crud import *
from modules.valuaciones.crud import *
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, status
from modules.helpers.errors import *
from modules.helpers.success import *
#ENRUTADOR#
valuacion = APIRouter()

##############################################################################################################
################################          VALUACIONES DE INSUMOS     #########################################
##############################################################################################################


@valuacion.get('/metodos_valuacion/', tags=["VALUACIÓN"])
def get_metodos_valorizacion(db: Session = Depends(get_db)):
    try:

        return db.query(Tipo_Metodo_Valorizacion).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@valuacion.get('/metodos_valuacion_empresas/', tags=["VALUACIÓN"])
def get_ver_metodos_valorizacion(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_Valorizacion_Empresas).all()

    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)


@valuacion.post('/metodo_valuacion/', tags=["VALUACIÓN"])
def elegir_metodo_valuacion(
    empresa_id: int,
    metodo_id: int,
    config: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    try:
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

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@valuacion.get('/valorizacion_entradas/', tags=["VALUACIÓN"])
def mostrar_valorizacin(insumo_id: int, db: Session = Depends(get_db)):
    try:
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

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@valuacion.get('/valorizacion_salidas/', tags=["VALUACIÓN"])
def mostrar_valorizacion(insumo_id: int, db: Session = Depends(get_db)):
    try:
        
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
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)
    
@valuacion.get('/valorizacion_saldo/', tags=["VALUACIÓN"])
def mostrar_valorizacion_total(insumo_id: int, db: Session = Depends(get_db)):
    try:
        
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
    
    except Exception as e:
        
        print(e)
        JSONResponse(error_1, 500)
            
###################################    MÉTODO PRECIO SEGÚN CRITERIO   ####################################################


@valuacion.post('/ingresar_cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def insumo_cotizacion(cotizacion: Cotizacion, db: Session = Depends(get_db)):
    try:
        
        return create_cotizacion(db=db, cotizacion=cotizacion)
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)

@valuacion.get('/cotizacion/', tags=['PRECIO SEGUN CRITERIO'])
def get_cotizacion(db: Session = Depends(get_db)):
    
    try:
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
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)