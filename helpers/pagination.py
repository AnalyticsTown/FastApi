import json
import random
import datetime
from sqlalchemy import func
from requests import session
from empresa.models import Alta_empresa_modelo
from insumo.schemas import *
from insumo.models import *
from insumo.crud import *
from fastapi import APIRouter
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.database import engine, get_db, Base  # , SessionLocal
from valuaciones.crud import *
import math

# def paginate(data, route: str, page_num: int = 1, page_size: int = 10):
#     #tomo el primer elemento del arreglo para la pagina
#     start = (page_num - 1) * page_size
#     #tomo el ultimo elemento del arreglo para la pagina
#     end = start + page_size
#     data_length = len(data)
#     response = {
#         "data": data[start:end],
#         "total_registros": data_length,
#         "total_paginas": math.ceil(data_length / page_size),
#         "cantidad_por_pagina": page_size,
#         "paginacion": {}
#     }
#     if end >= data_length:
#         response["paginacion"]["next"] = None
#         if start > 0:
#             response["paginacion"]["previous"] = f"/{route}?page_num={page_num-1}&page_size={page_size}"
#         else:
#             response["paginacion"]["previous"] = None
#     else:
#         if page_num > 1:
#             response["paginacion"]["previous"] = f"/{route}?page_num={page_num-1}&page_size={page_size}"
#         else:
#             response["paginacion"]["previous"] = None

#         response["paginacion"]["next"] = f"/{route}?page_num={page_num+1}&page_size={page_size}"

#     return response


def paginate(data: list, tabla: str, page_size: int, db: Session):
    statement = """
    --sql
    SELECT COUNT(*) FROM {tabla};
    """.format(tabla=tabla)
    total_registros = db.execute(statement).all()
    total_registros = jsonable_encoder(total_registros)
    total_registros = total_registros[0]["count"]
    response = {
        "data": data,
        "total_registros": total_registros,
        "total_paginas": math.ceil(total_registros/page_size),
        "cantidad_por_pagina": page_size
    }

    return response
