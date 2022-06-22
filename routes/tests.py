import datetime
import random
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from insumo.models import *
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, status

#ENRUTADOR#
test = APIRouter()

@test.post('/prueba_estres/', tags=['TESTING BACKEND'])
def ejecutar_prueba_estres(nro_pruebas: int, db: Session = Depends(get_db)):

    fecha = datetime.datetime.now()
    insumos_id = [1, 2, 3]
    for n in range(nro_pruebas):
        precio_unitario = random.random() * 100
        cantidad = int(random.random() * 1000)
        db_prueba = Stock_almacen_insumo_modelo(**{
            'cantidad': cantidad,
            'detalle': "string",
            'insumo_id': random.choice(insumos_id),
            'almacen_id': 2,
            'nro_lote': 'randomnrolote',
            'fecha_vencimiento': "{dia}-{mes}-{año}".format(dia=fecha.day, mes=fecha.month, año=fecha.year),
            'unidad_id': 1,
            'precio_unitario': precio_unitario,
            'precio_total': precio_unitario * cantidad
        })
        db.add(db_prueba)

    db.commit()
    db.refresh(db_prueba)
    return JSONResponse("Fake data creada exitosamente", 200)
