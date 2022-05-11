from typing import Union
#from fastapi.encoders import jsonable_encoder
#from fastapi.responses import JSONResponse
from fastapi import FastAPI#, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base  # , SessionLocal
from routes.usuario_sesion import usuario
from routes.almacen import almacen
from routes.empresa import empresa
from routes.establecimiento import establecimiento
from routes.facturacion import facturacion
from routes.insumo import insumo
from routes.lote import lote

#from mangum import Mangum

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


app.include_router(usuario)
app.include_router(almacen)
app.include_router(empresa)
app.include_router(establecimiento)
app.include_router(facturacion)
app.include_router(insumo)
app.include_router(lote)


#handler = mangum (app=app)
