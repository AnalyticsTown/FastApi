from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import math



def paginate(data: list, tabla: str, page_size: int, db: Session):
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
    response = {
        "data": data,
        "total_registros": total_registros,
        "total_paginas": math.ceil(total_registros/page_size),
        "cantidad_por_pagina": page_size
    }

    return response
