from modules.almacen.models import Alta_almacen_modelo, Tipo_almacen_modelo
from modules.empresa.models import Alta_empresa_modelo
from modules.facturacion.models import Alta_facturacion_modelo, Alta_tarjeta_emisor_modelo
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
from modules.lote.models import Alta_lote_modelo
from modules.usuario.models import Alta_auditoria_modelo, Alta_rol_modelo, Alta_usuario_modelo
from modules.valuaciones.crud import *
from modules.helpers.errors import *
from modules.helpers.success import *
from modules.establecimiento.models import *

sincro = APIRouter()

######################################################################################################################
################################################# ALMACENES ##########################################################
######################################################################################################################


@sincro.get('/sincro_almacenes', tags=["SINCRONIZACION"])
def get_almacen_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_almacen_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_tipo_almecenes', tags=["SINCRONIZACION"])
def get_tipo_almacenes_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_almacen_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)


##############################################################################################################
#############################################  EMPRESAS  #####################################################
##############################################################################################################
@sincro.get('/sincro_empresas', tags=['SINCRONIZACION'])
def get_sincro_empresas(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_empresa_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)

###############################################################################################################
#########################################  ESTABLECIMIENTOS  ##################################################
###############################################################################################################


@sincro.get('/sincro_establecimientos', tags=["SINCRONIZACION"])
def get_establecimientos_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_establecimiento_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


################################################################
#################### FACTURACION ###############################
################################################################
@sincro.get("/sincro_facturaciones", tags=['SINCRONIZACION'])
def get_facturacion_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_facturacion_modelo).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)

################################################################
######################      INSUMOS     ########################
################################################################


@sincro.get('/sincro_insumos', tags=["SINCRONIZACION"])
def get_insumos_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_insumo_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)

################################################################
###################### LOTE ####################################
################################################################


@sincro.get('/sincro_lotes', tags=["SINCRONIZACION"])
def get_lotes_sincro(db: Session = Depends(get_db)):
    try:
        db.query(Alta_lote_modelo).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)

################################################################
###################  MOVIMIENTOS DE STOCK ######################
################################################################


@sincro.get('/sincro_movimiento_detalle', tags=["SINCRONIZACION"])
def get_movimiento_detalle_sincro(db: Session = Depends(get_db)):
    try:
        return db.query(Movimiento_detalle_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_encabezado_movimiento', tags=["SINCRONIZACION"])
def get_movimiento_encabezado(db: Session = Depends(get_db)):
    try:
        return db.query(Encabezado_insumos_modelo).all()
    except Exception as e:
        return JSONResponse(error_1, 500)
    
##################################################################
######################## STOCKS ##################################
##################################################################

@sincro.get('/sincro_emisor_tarjetas', tags=["SINCRONIZACION"])
def get_emisor_tarjeta(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_tarjeta_emisor_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_usuarios', tags=["SINCRONIZACION"])
def get_usuarios(db: Session = Depends(get_db)):

    try:
        return db.query(Alta_usuario_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_roles', tags=["SINCRONIZACION"])
def get_roles_modelos(db: Session = Depends(get_db)):

    try:
        return db.query(Alta_rol_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_log_auditoria_usuarios', tags=['SINCRONIZACION'])
def get_auditoria_usuarios(db: Session = Depends(get_db)):
    try:
        return db.query(Alta_auditoria_modelo).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_insumos_valorizacion', tags=['SINCRONIZACION'])
def get_insumos_valorizacion(db: Session = Depends(get_db)):
    try:

        return db.query(Insumos_valorizacion).all()

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_tipo_metodo_valorizacion', tags=['SINCRONIZACION'])
def get_tipo_metodo_valorizacion(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_Metodo_Valorizacion).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_tipo_valorizacion_empresas', tags=['SINCRONIZACION'])
def get_tipo_valorizacion_empresas(db: Session = Depends(get_db)):
    try:
        return db.query(Tipo_Valorizacion_Empresas).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)


@sincro.get('/sincro_historicos_precio_segun_criterio', tags=["SINCRONIZACION"])
def get_historicos_precio_segun_criterio(db: Session = Depends(get_db)):
    try:
        return db.query(Historicos_Precio_Segun_Criterio).all()
    except Exception as e:
        print(e)
        return JSONResponse(error_1, 500)
