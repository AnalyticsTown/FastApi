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
from modules.helpers.pagination import pagination_sql
stock = APIRouter()

##############################################################################################################
################################          stocks (STOCKS)       #########################################
##############################################################################################################


@stock.get("/stocks/", tags=['stocks'])
def get_movimiento_insumos(id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        text = pagination_sql(id=id)

        statement = """
                        --sql
                        SELECT 
                        stocks.id,
                        insumos.nombre AS insumo,
                        insumos.reposicion_alerta,
                        insumos.reposicion_control,
                        insumos.reposicion_cantidad,
                        stocks.precio_unitario,
                        stocks.fecha_vencimiento,
                        stocks.nro_lote,
                        almacenes.nombre AS almacen,
                        unidades.abr AS unidad,
                        stocks.detalle AS detalle,
                        stocks.cantidad AS cantidad
                        FROM stocks
                        LEFT JOIN insumos ON insumos.id = stocks.insumo_id
                        LEFT JOIN almacenes ON almacenes.id = stocks.almacen_id
                        LEFT JOIN unidades ON unidades.id = stocks.unidad_id
                        {text};
                        """.format(text=" ")

        response = db.execute(statement).all()
        return JSONResponse(response, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@stock.get("/stocks/total/", tags=['stocks'])
def get_stocks_total(id: Optional[int] = None, total: Optional[bool] = None, db: Session = Depends(get_db)):
    try:
        if id:
            statement = """
                    --sql
                    SELECT 
                    stocks.precio_total,
                    almacenes.nombre,
                    insumos.nombre AS insumo,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    unidades.abr AS unidad,
                    stocks.fecha_vencimiento,
                    SUM(stocks.cantidad) total
                    FROM stocks
                    LEFT JOIN insumos ON insumos.id = stocks.insumo_id
                    LEFT JOIN unidades ON unidades.id = stocks.unidad_id
                    LEFT JOIN almacenes ON almacenes.id = stocks.almacen_id
                    WHERE stocks.almacen_id = {id}
                    GROUP BY insumo, 
                    insumos.reposicion_control, 
                    insumos.reposicion_cantidad, 
                    unidad, 
                    almacenes.nombre, 
                    stocks.precio_total, 
                    stocks.fecha_vencimiento;       
            """.format(id=id)

        elif total == True:

            statement = """
                    --sql
                    SELECT 
                    insumos.nombre AS insumo,
                    insumos.reposicion_control,
                    insumos.reposicion_cantidad,
                    unidades.abr AS unidad,
                    SUM(stocks.cantidad) total
                    FROM stocks
                    LEFT JOIN insumos ON insumos.id = stocks.insumo_id
                    LEFT JOIN unidades ON unidades.id = stocks.unidad_id
                    LEFT JOIN almacenes ON almacenes.id = stocks.almacen_id
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
                    SUM(stocks.cantidad) total
                    FROM stocks
                    LEFT JOIN insumos ON insumos.id = stocks.insumo_id
                    LEFT JOIN unidades ON unidades.id = stocks.unidad_id
                    LEFT JOIN almacenes ON almacenes.id = stocks.almacen_id
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


@stock.delete('/stocks_desarrollo/', tags=['stocks'])
def borrar_stocks(db: Session = Depends(get_db)):

    db.query(Stock_almacen_insumo_modelo).delete()
    db.commit()

    return "Existencia eliminadas"
