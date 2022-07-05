from urllib import response
from modules.helpers.pagination import paginate
from modules.insumo.schemas import *
from modules.insumo.models import *
from modules.insumo.crud import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from modules.valuaciones.crud import *
from modules.stocks.crud import *
from modules.stocks.crud_movimientos_stock import *
from modules.helpers.errors import *
from modules.helpers.success import *
movimiento = APIRouter()

##############################################################################################################
################################  MOVIMIENTOS ENCABEZADO Y DETALLE   #########################################
##############################################################################################################


###################################    ENCABEZADO CRUD    ####################################################

@movimiento.get("/encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def get_encabezado_movimiento(page_size: int = 10, page_num: int = 1, db: Session = Depends(get_db)):
    try:
        movimiento = get_movimiento_encabezado(
            db=db, page_size=page_size, page_num=page_num)

        return paginate(data=movimiento, tabla="encabezado_movimiento", page_size=page_size, db=db)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@movimiento.post("/create_encabezado_movimiento/", tags=['ENCABEZADO MOVIMIENTO'])
def create_encabezado(encabezado: EncabezadoInsumos, db: Session = Depends(get_db)):
    try:

        return create_encabezado_movimiento(db=db, encabezado=encabezado)

    except:

        return JSONResponse(error_1, 500)


@movimiento.delete('/encabezado_movimiento_desarrollo/', tags=['ENCABEZADO MOVIMIENTO'])
def borrar_encabezados(db: Session = Depends(get_db)):
    try:
        statement = """
            --sql
            TRUNCATE TABLE encabezado_movimiento CASCADE;
            """
        db.execute(statement)
        db.commit()

        return "encabezados eliminados"

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@movimiento.delete('/encabezado_movimiento/', tags=['ENCABEZADO MOVIMIENTO'])
def delete_encabezados(id: int, db: Session = Depends(get_db)):
    try:
        db.query(Encabezado_insumos_modelo).filter_by(id=id).\
            update({
                Encabezado_insumos_modelo.deleted_at: datetime.datetime.now()
            })
        return JSONResponse(success_3, 500)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


###################################    DETALLE  CRUD    ####################################################

@movimiento.get('/movimiento_detalle/', tags=['DETALLE-MOVIMIENTO'])
def movimiento_detalle(page_num: Optional[int] = None, page_size: Optional[int] = None, id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        response = get_movimiento_detalle(
            db=db,
            page_num=page_num,
            page_size=page_size,
            id=id
        )
        return JSONResponse(response, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@movimiento.post("/create_movimiento_detalle/",  status_code=status.HTTP_201_CREATED, tags=['DETALLE-MOVIMIENTO'])
def crear_movimiento_insumo(movimiento: MovimientoDetalleBase, db: Session = Depends(get_db)):

    try:
        # busco el encabezado y lo encuentro
        encabezado = db.query(Encabezado_insumos_modelo).filter_by(
            id=movimiento.encabezado_movimiento_id).first()
        # transformo la respuesta en un json
        encabezado2 = jsonable_encoder(encabezado)
        # busco el insumo asociado al detalle
        insumo = db.query(Alta_insumo_modelo).filter_by(
            id=movimiento.insumo_id).first()
        insumo = jsonable_encoder(insumo)

        if encabezado2['tipo_movimiento_id'] == 1:
            # si el encabezado es una compra
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
            # si el encabezado es un ajuste
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
        # Despues de enviar los datos necesarios para actualizar stock creo el detalle
        response = create_movimiento_detalle(db=db, movimiento={
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

        return JSONResponse(response, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@movimiento.delete("/delete_movimiento_detalle/{id}", tags=['DETALLE-MOVIMIENTO'])
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

        return JSONResponse(success_1, 500)


@movimiento.delete("/delete_movimiento_detalle/{id}", tags=['DETALLE-MOVIMIENTO'])
def delete_movimiento_insumo(id: int, db: Session = Depends(get_db)):
    try:

        if id:
            db.query(Movimiento_detalle_modelo).filter(Movimiento_detalle_modelo.id == id).\
                update({
                    Movimiento_detalle_modelo.deleted_at: datetime.datetime.now()
                })

            db.commit()

        return JSONResponse(success_3, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)

#################################################((***))######################################################
