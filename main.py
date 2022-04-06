from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, get_db, Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#%% Es para crear la base de datos. Importo todos los modelos
from empresa.models import *
from usuario.models import *
from establecimiento.models import *
from almacen.models import *
from insumo.models import *
from facturacion.models import *
from tablas_secundarias.models import *
#%%

from empresa.schemas import *
from empresa.crud import *
from establecimiento.schemas import *
from establecimiento.crud import *
from almacen.schemas import *
from almacen.crud import *
from facturacion.schemas import *
from facturacion.crud import *
from insumo.schemas import *
from insumo.crud import *

Base.metadata.create_all(bind=engine)



@app.post("/create_empresas/", response_model=Empresa, status_code=status.HTTP_201_CREATED)
def crear_empresa(empresa: EmpresaBase, db: Session = Depends(get_db)):
    db_empresa = get_empresa(db, razon=empresa.razon_social, pais=empresa.direccion_pais)
    if db_empresa:
        raise HTTPException(status_code=400, detail="La empresa ya existe!")
    if empresa.direccion_pais.casefold() == 'argentina':
        if empresa.cuit == None:
            raise HTTPException(status_code=400, detail="Completar CUIT")
        if empresa.cond_iva_id == None:
            raise HTTPException(status_code=400, detail="Completar condición ante el IVA ")
    return create_empresa(db=db, empresa=empresa)

@app.get("/empresas/", response_model=list[Empresa])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empresas = get_empresas(db, skip=skip, limit=limit)
    return empresas

@app.delete("/delete_empresas")
def delete_empresas(db: Session = Depends(get_db)):
    drop_empresas(db)
    return "Las empresas fueron borradas"

@app.post("/create_establecimientos/", response_model=Establecimiento, status_code=status.HTTP_201_CREATED)
def crear_establecimiento(establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    db_establecimiento = get_establecimiento(db, localidad=establecimiento.localidad, direccion=establecimiento.direccion)
    if db_establecimiento:
        raise HTTPException(status_code=400, detail="El establecimiento ya existe!")
    return create_establecimiento(db=db, establecimiento=establecimiento)

@app.get("/establecimientos/", response_model=list[Establecimiento])
def read_establecimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    establecimientos = get_establecimientos(db, skip=skip, limit=limit)
    return establecimientos

@app.delete("/delete_establecimientos")
def delete_establecimientos(db: Session = Depends(get_db)):
    drop_establecimientos(db)
    return "Los establecimientos fueron borrados"

@app.post("/create_almacenes/", response_model=Almacen, status_code=status.HTTP_201_CREATED)
def crear_almacen(almacen: AlmacenBase, db: Session = Depends(get_db)):
    db_almacen = get_almacen(db, nombre=almacen.nombre, establecimiento_id=almacen.establecimiento_id)
    if db_almacen:
        raise HTTPException(status_code=400, detail="El almacen ya existe!")
    return create_almacen(db=db, almacen=almacen)

@app.get("/almacenes/", response_model=list[Almacen])
def read_almacenes(db: Session = Depends(get_db)):
    almacenes = get_almacenes(db)
    return almacenes

@app.delete("/delete_almacenes")
def delete_almacenes(db: Session = Depends(get_db)):
    drop_almacenes(db)
    return "Los almacenes fueron borrados"

@app.post("/create_facturaciones/", response_model=Facturacion, status_code=status.HTTP_201_CREATED)
def crear_facturacion(facturacion: FacturacionBase, db: Session = Depends(get_db)):
    db_facturacion = get_facturacion(db, nro_tarjeta=facturacion.nro_tarjeta)
    if db_facturacion:
        raise HTTPException(status_code=400, detail="La tarjeta ya existe!")
    return create_facturacion(db=db, facturacion=facturacion)

@app.get("/facturaciones/", response_model=list[Facturacion])
def read_facturaciones(db: Session = Depends(get_db)):
    facturaciones = get_facturaciones(db)
    return facturaciones

@app.delete("/delete_facturaciones")
def delete_facturaciones(db: Session = Depends(get_db)):
    drop_facturaciones(db)
    return "Las facturaciones fueron borradas"

@app.post("/create_insumos/", response_model=Insumo, status_code=status.HTTP_201_CREATED)
def crear_insumo(insumo: InsumoBase, db: Session = Depends(get_db)):
    db_insumo = get_insumo(db, nombre=insumo.nombre)
    if db_insumo:
        raise HTTPException(status_code=400, detail="El insumo ya existe!")
    return create_insumo(db=db, insumo=insumo)

@app.get("/insumos/", response_model=list[Insumo])
def read_insumos(db: Session = Depends(get_db)):
    insumos = get_insumos(db)
    return insumos

@app.delete("/delete_insumos")
def delete_insumos(db: Session = Depends(get_db)):
    drop_insumos(db)
    return "Los insumos fueron borrados"
