from modules.facturacion.models import Alta_tarjeta_emisor_modelo
from modules.helpers.pagination import paginate
from modules.insumo.schemas import *
from modules.insumo.models import *
from modules.insumo.crud import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from modules.usuario.models import Alta_auditoria_modelo, Alta_rol_modelo, Alta_usuario_modelo
from modules.valuaciones.crud import *
from modules.helpers.errors import *
from modules.helpers.success import *
from modules.establecimiento.models import *

sincro = APIRouter()


@sincro.get('/emisor_tarjetas', tags=["SINCRONIZACION"])
def get_emisor_tarjeta(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_tarjeta_emisor_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/establecimientos', tags=["SINCRONIZACION"])
def get_establecimientos_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_establecimiento_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/usuarios', tags=["SINCRONIZACION"])
def get_usuarios(db: Session = Depends(get_db)):

    try:
        return db.query(Alta_usuario_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/usuarios', tags=["SINCRONIZACION"])
def get_roles_modelos(db: Session = Depends(get_db)):

    try:
        return db.query(Alta_rol_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/log_auditoria_usuarios', tags=['SINCRONIZACION'])
def get_auditoria_usuarios(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_auditoria_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/insumos_valorizacion', tags=['SINCRONIZACION'])
def get_insumos_valorizacion(db: Session = Depends(get_db)):
    try:

        return db.query(Insumos_valorizacion).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/tipo_metodo_valorizacion', tags=['SINCRONIZACION'])
def get_tipo_metodo_valorizacion(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_Metodo_Valorizacion).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/tipo_valorizacion_empresas', tags=['SINCRONIZACION'])
def get_tipo_valorizacion_empresas(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_Valorizacion_Empresas).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/historicos_precio_segun_criterio', tags=["SINCRONIZACION"])
def get_historicos_precio_segun_criterio(db: Session = Depends(get_db)):
    try:
        return db.query(Historicos_Precio_Segun_Criterio).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)
