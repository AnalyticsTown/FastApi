from pydantic import Json
from modules.establecimiento.schemas import *
from modules.establecimiento.models import *
from modules.establecimiento.crud import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db

establecimiento = APIRouter()

##############################################################################################################
################################        CRUD ESTABLECIMIENTO       ###########################################
##############################################################################################################


@establecimiento.get("/{empresa_id}/establecimientos/", tags=['ESTABLECIMIENTO'])
async def read_establecimientos(empresa_id: int, db: Session = Depends(get_db)):
    establecimientos = get_establecimientos(db, empresa=empresa_id)
    return JSONResponse(jsonable_encoder(establecimientos))


@establecimiento.post("/{empresa_id}/create_establecimientos/",  status_code=status.HTTP_201_CREATED, tags=['ESTABLECIMIENTO'])
def crear_establecimiento(empresa_id: int, establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    db_establecimiento = get_establecimiento(
        db, localidad=establecimiento.localidad, nombre=establecimiento.nombre)
    if db_establecimiento:
        raise HTTPException(
            status_code=400, detail="El establecimiento ya existe!")
    create_establecimiento(
        db=db, establecimiento=establecimiento, empresa_id=empresa_id)
    return JSONResponse("Establecimiento creado exitosamente", status_code=200)


@establecimiento.put("/{empresa_id}/update_establecimiento/", status_code=status.HTTP_200_OK, tags=['ESTABLECIMIENTO'])
def update_establecimiento(empresa_id: int, establecimiento_id: int, establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    try:
        db.query(Alta_establecimiento_modelo).filter_by(id=establecimiento_id, empresa_id=empresa_id).\
            update({
                #Alta_establecimiento_modelo.activo: establecimiento.activo,
                Alta_establecimiento_modelo.nombre: establecimiento.nombre,
                Alta_establecimiento_modelo.abreviatura: establecimiento.abreviatura,
                Alta_establecimiento_modelo.direccion: establecimiento.direccion,
                Alta_establecimiento_modelo.localidad: establecimiento.localidad,
                Alta_establecimiento_modelo.provincia: establecimiento.provincia,
                Alta_establecimiento_modelo.pais: establecimiento.pais,
                Alta_establecimiento_modelo.geoposicion: establecimiento.geoposicion,
                Alta_establecimiento_modelo.observaciones: establecimiento.observaciones,
                Alta_establecimiento_modelo.contacto: establecimiento.contacto,
                Alta_establecimiento_modelo.zona_id: establecimiento.zona_id,
                #Alta_establecimiento_modelo.empresa_id: establecimiento.empresa_id,
                Alta_establecimiento_modelo.establecimiento_tipo_id: establecimiento.establecimiento_tipo_id,
                #Alta_establecimiento_modelo.almacenes: establecimiento.almacen_id
            })
        db.commit()
        return JSONResponse({"response": "EL establecimiento fue actualizado"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(e, status_code=404)


@establecimiento.delete("/delete_establecimientos/", tags=['ESTABLECIMIENTO'])
def delete_establecimientos(db: Session = Depends(get_db)):
    drop_establecimientos(db)
    return "Los establecimientos fueron borrados"


@establecimiento.get("/establecimiento/zonas/", 
                     response_model=list[Zona], 
                     tags=['SOLO LECTURA'])
def read_zonas(db: Session = Depends(get_db)):
    zonas = get_zonas(db)
    return zonas


@establecimiento.get("/establecimiento/tipo_establecimientos/", 
                     response_model=list[TipoEstablecimiento], 
                     tags=['SOLO LECTURA'])
def read_tipo_establecimientos(db: Session = Depends(get_db)):
    tipo_establecimientos = get_tipo_establecimientos(db)
    return tipo_establecimientos

################################################################(***)################################################################