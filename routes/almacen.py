from modules.almacen.schemas import *
from modules.almacen.models import *
from modules.almacen.crud import *
from modules.helpers.pagination import paginate
from modules.helpers.errors import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db

almacen = APIRouter()

##############################################################################################################
################################        CRUD ALMACENES     ###################################################
##############################################################################################################


@almacen.get("/almacenes/", tags=['ALMACEN'])
def read_almacenes(page_num: Optional[int] = None, page_size: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        
        almacenes = get_almacenes(db=db, page_num=page_num, page_size=page_size)
        response = paginate(
                            db=db, 
                            data=almacenes,
                            tabla="almacenes", 
                            page_size=page_size
                            )
        
        return JSONResponse(response, 200)
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)


@almacen.post("/create_almacenes", response_model=AlmacenBase, status_code=status.HTTP_201_CREATED, tags=['ALMACEN'])
def crear_almacen(almacen: AlmacenBase, db: Session = Depends(get_db)):
    try:
        
        db_almacen = get_almacen(db, nombre=almacen.nombre)
        if db_almacen:
            raise HTTPException(status_code=400, detail="El almacen ya existe!")
        
        response = create_almacen(db=db, almacen=almacen)
        return response
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)
    
@almacen.put('/update_almacen/', tags=["ALMACEN"])
def update_almacen(almacen: AlmacenBase, id: int, db: Session = Depends(get_db)):
    try:
    
        db.query(Alta_almacen_modelo).\
            filter_by(id=id).\
            update({
                Alta_almacen_modelo.nombre: almacen.nombre,
                Alta_almacen_modelo.abreviatura: almacen.abreviatura,
                Alta_almacen_modelo.descripcion: almacen.descripcion,
                Alta_almacen_modelo.geoposicion: almacen.geoposicion,
                Alta_almacen_modelo.observaciones: almacen.observaciones,
                Alta_almacen_modelo.almacenes_tipo_id: almacen.almacenes_tipo_id
            })
        db.commit()
        return JSONResponse("Almacen actualizado", 200)
    
    except Exception as e:
        
        print(e)
        return JSONResponse("Hubo un error", 500)


@almacen.delete("/delete_almacenes/", tags=['ALMACEN'])
def delete_almacenes(id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        
        if id:
        
            db.query(Alta_almacen_modelo).filter_by(id=id).\
                delete(synchronize_session=False)
            db.commit()
            
            return JSONResponse({'response': "El Almacen eliminado"})
        
        else:
        
            statement = """
            --sql
            TRUNCATE TABLE establecimiento_almacenes cascade;
            """
            db.execute(statement)
            statement = """
            --sql
            TRUNCATE TABLE almacenes CASCADE;
            """
            db.execute(statement)
            db.commit()
            
            return JSONResponse({'response': "Almacenes eliminados"})
    
    except Exception as e:
        
        print(e)
        return JSONResponse({'response': "El Almacen posee información relacionada para ser eliminado"}, 500)


@almacen.get("/almacen/tipo_almacenes/", response_model=list[TipoAlmacen], tags=['ALMACEN'])
def read_tipo_almacenes(db: Session = Depends(get_db)):
    
    try:
                
        tipo_almacenes = get_tipo_almacenes(db)
        return tipo_almacenes 
    
    except Exception as e:
        
        print(e)
        return JSONResponse(error_1, 500)
