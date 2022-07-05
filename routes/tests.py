import string
import datetime
import random
from randomtimestamp import randomtimestamp
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modules.insumo.models import *
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import Depends

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


@test.post('/test_insumos/', tags=['TESTING BACKEND'])
def cargar_insumos(nro_pruebas: int, db: Session = Depends(get_db)):
    N = 5
    for n in range(nro_pruebas):
        db_prueba = Alta_insumo_modelo(**{
            'nombre': str(''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N))),
            'abreviatura': "RANDOM",
            'codigo_externo': "str",
            'lote_control': random.choice([True, False]),
            'vencimiento_control': random.choice([True, False]),
            'reposicion_control': random.choice([True, False]),
            'reposicion_cantidad': random.choice([100, 50, 20]),
            'reposicion_alerta': random.choice([True, False]),
            'reposicion_alerta_email': "user@example.com",
            'tarea_id': random.choice([1, 2]),
            'unidad_id': random.choice([1, 2]),
            'familia_id': random.choice([1, 2]),
            'subfamilia_id': random.choice([1, 2]),
            'rubro_insumo_id': random.choice([1, 2]),
            'tipo_erogacion_id': random.choice([1, 2]),
            'created_at': randomtimestamp()
        })
        db.add(db_prueba)
    
    db.commit()
    db.refresh(db_prueba)
    return JSONResponse("Fake data creada exitosamente", 200)
