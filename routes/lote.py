from modules.lote.schemas import *
from modules.lote.models import *
from modules.lote.crud import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from modules.helpers.errors import *

lote = APIRouter()

##############################################################################################################
################################        CRUD LOTE       ###################################################
##############################################################################################################


@lote.get("/lotes/", response_model=list[Lote], tags=['LOTE'])
def read_lotes(db: Session = Depends(get_db)):
    try:

        lotes = get_lotes(db)
        return JSONResponse(lotes, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@lote.post("/create_lotes/", response_model=Lote, status_code=status.HTTP_201_CREATED, tags=['LOTE'])
def crear_lote(lote: LoteBase, db: Session = Depends(get_db)):
    try:

        db_lote = get_lote(db, codigo=lote.codigo)
        if db_lote:
            raise HTTPException(status_code=400, detail="El lote ya existe!")
        response = create_lote(db=db, lote=lote)

        return JSONResponse(response, 200)

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)


@lote.delete("/delete_lotes/", tags=['LOTE'])
def delete_lotes(db: Session = Depends(get_db)):
    try:

        drop_lotes(db)
        return "Los lotes fueron borrados"

    except Exception as e:

        print(e)
        return JSONResponse(error_1, 500)

#############################################(***)#############################################################
