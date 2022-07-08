from importlib.metadata import packages_distributions
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional
import math


def paginate(db: Session, data: list, tabla: str, page_size: Optional[int] = None):
    # calculo el total filas
    statement = """
    --sql
    SELECT COUNT(*) FROM {tabla};
    """.format(tabla=tabla)
    # parseo a json
    total_registros = db.execute(statement).all()
    total_registros = jsonable_encoder(total_registros)

    # accedo al diccionario
    total_registros = total_registros[0]["count"]

    if page_size is None:
        page_size = total_registros
    if total_registros == 0:
        page_size = 1
    response = {
        "data": data,
        "total_registros": total_registros,
        "total_paginas": math.ceil(total_registros/page_size),
        "cantidad_por_pagina": page_size
    }

    return response


def pagination_sql(page_size: int, page_num: int):
    
    if page_size and page_num:

        text = """LIMIT {page_size}
                OFFSET ({page_num} - 1) * {page_size};        
            """.format(page_size=page_size, page_num=page_num)

    else:

        text = " "

    return text
