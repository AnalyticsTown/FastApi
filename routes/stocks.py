from modules.insumo.schemas import *
from modules.insumo.models import *
from modules.insumo.crud import *
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from modules.valuaciones.crud import *
from modules.helpers.errors import * 
from modules.helpers.success import *

stock = APIRouter()

##############################################################################################################
################################          EXISTENCIAS (STOCKS)       #########################################
##############################################################################################################


@stock.get("/existencias/", tags=['EXISTENCIAS'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
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
                        {text};
                        """

        if id:
        
            text = "WHERE stock_almacen_insumos.almacen_id = {id}".format(id=id)
            statement.format(text=text)
        
        else:
        
            statement.format(text=" ")

        response = db.execute(statement).all()       
        return JSONResponse(response, 200)
    
    except Exception as e:
        
        print(e)
        return JSONResponse()

@stock.get("/existencias/total/", tags=['EXISTENCIAS'])
def get_existencias_total(id: Optional[int] = None, total: Optional[bool] = None, db: Session = Depends(get_db)):
    try:
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
                
        response = db.execute(statement).all()
        return JSONResponse(response, 200)
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)

@stock.delete('/existencias_desarrollo/', tags=['EXISTENCIAS'])
def borrar_existencias(db: Session = Depends(get_db)):
    db.query(Stock_almacen_insumo_modelo).delete()
    db.commit()
    return "Existencia eliminadas"
