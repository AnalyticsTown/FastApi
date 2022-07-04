from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import math
from typing import Optional


def paginate(db: Session, data: list, tabla: str, page_size: Optional[int] = None):
    #calculo el total filas
    statement = """
    --sql
    SELECT COUNT(*) FROM {tabla};
    """.format(tabla=tabla)
    #parseo a json
    total_registros = db.execute(statement).all()
    total_registros = jsonable_encoder(total_registros)
    
    #accedo al diccionario
    total_registros = total_registros[0]["count"]
    
    if page_size is None:
        page_size = total_registros

    response = {
        "data": data,
        "total_registros": total_registros,
        "total_paginas": math.ceil(total_registros/page_size),
        "cantidad_por_pagina": page_size
    }

    return response
