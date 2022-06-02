from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from insumo import models, schemas
from sqlalchemy import update
import datetime
import json
from valuaciones.models import *

def create_valorizacion_compra(
    db: Session,
    cantidad: int,
    precio_unitario: float,
    almacen_id: int,
    movimiento_entrada: str,
    movimiento_salida: str
):


    precio_total = cantidad * precio_unitario
     
    db_valorizacion = Insumos_valorizacion(**{
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "precio_total": precio_total,
        "almacen_id": almacen_id,
        "movimiento_entrada": movimiento_entrada,
        "movimiento_salida": movimiento_salida
    })
    db.add(db_valorizacion)
    db.commit()
    db.refresh(db_valorizacion)
    

    
