from modules.facturacion.schemas import *
from modules.facturacion.models import *
from modules.facturacion.crud import *
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db

facturacion = APIRouter()

##############################################################################################################
#########################################  FACTURACION   ###################################################
##############################################################################################################


@facturacion.get("/facturaciones/", response_model=list[Facturacion], tags=['FACTURACION'])
def read_facturaciones(db: Session = Depends(get_db)):
    facturaciones = get_facturaciones(db)
    return facturaciones


@facturacion.post("/create_facturaciones/", response_model=Facturacion, status_code=status.HTTP_201_CREATED, tags=['FACTURACION'])
def crear_facturacion(facturacion: FacturacionBase, db: Session = Depends(get_db)):
    db_facturacion = get_facturacion(db, nro_tarjeta=facturacion.nro_tarjeta)
    if db_facturacion:
        raise HTTPException(status_code=400, detail="La tarjeta ya existe!")
    return create_facturacion(db=db, facturacion=facturacion)


@facturacion.put("/update_facturacion/", tags=['FACTURACION'])
def update_facturacion(facturacion: FacturacionBase, id: int, db: Session = Depends(get_db)):
    try:
        db.query(Alta_facturacion_modelo).filter_by(id=id).\
            update({
                Alta_facturacion_modelo.nro_tarjeta: facturacion.nro_tarjeta,
                Alta_facturacion_modelo.vto_fecha: facturacion.vto_fecha,
                Alta_facturacion_modelo.cod_verificacion: facturacion.cod_verificacion,
                # Alta_facturacion_modelo.fecha_alta: facturacion.fecha_alta,
                # Alta_facturacion_modelo.fecha_baja: facturacion.fecha_baja,
                Alta_facturacion_modelo.tarjeta_emisor_id: facturacion.tarjeta_emisor_id,
            })
        db.commit()
        return JSONResponse({"response": "Facturación actualizada"}, status_code=200)
    
    except Exception as e:
        
        print(e)
        return JSONResponse({"response": "Ocurrió un error"}, status_code=500)


@facturacion.delete("/delete_facturaciones/", tags=['FACTURACION'])
def delete_facturaciones(db: Session = Depends(get_db)):
    drop_facturaciones(db)
    return "Las facturaciones fueron borradas"

########################################((***))##########################################################
