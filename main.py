from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, get_db, Base #, SessionLocal

#%% Es para crear la base de datos. Importo todos los modelos
from empresa.models import *
from usuario.models import *
from establecimiento.models import *
from almacen.models import *
from insumo.models import *
from facturacion.models import *
from tablas_relacionales.models import *
from lote.models import *

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
from lote.schemas import *
from lote.crud import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

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
def read_empresas(db: Session = Depends(get_db)):
    empresas = get_empresas(db)
    return empresas

@app.delete("/delete_empresas/")
def delete_empresas(db: Session = Depends(get_db)):
    drop_empresas(db)
    return "Las empresas fueron borradas"

@app.post("/create_establecimientos/", response_model=Establecimiento, status_code=status.HTTP_201_CREATED)
def crear_establecimiento(establecimiento: EstablecimientoBase, db: Session = Depends(get_db)):
    db_establecimiento = get_establecimiento(db, localidad=establecimiento.localidad, nombre=establecimiento.nombre)
    if db_establecimiento:
        raise HTTPException(status_code=400, detail="El establecimiento ya existe!")
    return create_establecimiento(db=db, establecimiento=establecimiento)

@app.get("/establecimientos/", response_model=list[Establecimiento])
def read_establecimientos(db: Session = Depends(get_db)):
    establecimientos = get_establecimientos(db)
    return establecimientos

@app.delete("/delete_establecimientos/")
def delete_establecimientos(db: Session = Depends(get_db)):
    drop_establecimientos(db)
    return "Los establecimientos fueron borrados"

@app.post("/create_almacenes/", response_model=Almacen, status_code=status.HTTP_201_CREATED)
def crear_almacen(almacen: AlmacenBase, db: Session = Depends(get_db)):
    db_almacen = get_almacen(db, nombre=almacen.nombre)
    if db_almacen:
        raise HTTPException(status_code=400, detail="El almacen ya existe!")
    return create_almacen(db=db, almacen=almacen)

@app.get("/almacenes/", response_model=list[Almacen])
def read_almacenes(db: Session = Depends(get_db)):
    almacenes = get_almacenes(db)
    return almacenes

@app.delete("/delete_almacenes/")
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

@app.delete("/delete_facturaciones/")
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

@app.delete("/delete_insumos/")
def delete_insumos(db: Session = Depends(get_db)):
    drop_insumos(db)
    return "Los insumos fueron borrados"

@app.post("/create_lotes/", response_model=Lote, status_code=status.HTTP_201_CREATED)
def crear_lote(lote: LoteBase, db: Session = Depends(get_db)):
    db_lote = get_lote(db, codigo=lote.codigo)
    if db_lote:
        raise HTTPException(status_code=400, detail="El lote ya existe!")
    return create_lote(db=db, lote=lote)

@app.get("/lotes/", response_model=list[Lote])
def read_lotes(db: Session = Depends(get_db)):
    lotes = get_lotes(db)
    return lotes

@app.delete("/delete_lotes/")
def delete_lotes(db: Session = Depends(get_db)):
    drop_lotes(db)
    return "Los lotes fueron borrados"

@app.get("/almacen/tipo_almacenes/", response_model=list[TipoAlmacen])
def read_tipo_almacenes(db: Session = Depends(get_db)):
    tipo_almacenes = get_tipo_almacenes(db)
    return tipo_almacenes

@app.get("/empresa/cond_ivas/", response_model=list[CondicionIva])
def read_cond_ivas(db: Session = Depends(get_db)):
    cond_ivas = get_cond_ivas(db)
    return cond_ivas

@app.get("/empresa/rubro_empresas/", response_model=list[RubroEmpresa])
def read_rubro_empresas(db: Session = Depends(get_db)):
    rubro_empresas = get_rubro_empresas(db)
    return rubro_empresas

@app.get("/empresa/monedas/", response_model=list[Moneda])
def read_monedas(db: Session = Depends(get_db)):
    monedas = get_monedas(db)
    return monedas

@app.get("/establecimiento/zonas/", response_model=list[Zona])
def read_zonas(db: Session = Depends(get_db)):
    zonas = get_zonas(db)
    return zonas

@app.get("/establecimiento/tipo_establecimientos/", response_model=list[TipoEstablecimiento])
def read_tipo_establecimientos(db: Session = Depends(get_db)):
    tipo_establecimientos = get_tipo_establecimientos(db)
    return tipo_establecimientos

@app.get("/insumo/tareas/", response_model=list[Tarea])
def read_tareas(db: Session = Depends(get_db)):
    tareas = get_tareas(db)
    return tareas

@app.get("/insumo/unidades/", response_model=list[Unidad])
def read_unidades(db: Session = Depends(get_db)):
    unidades = get_unidades(db)
    return unidades

@app.get("/insumo/familias/", response_model=list[Familia])
def read_familias(db: Session = Depends(get_db)):
    familias = get_familias(db)
    return familias

@app.get("/insumo/subfamilias/", response_model=list[Subfamilia])
def read_subfamilias(db: Session = Depends(get_db)):
    subfamilias = get_subfamilias(db)
    return subfamilias

@app.get("/insumo/rubro_insumos/", response_model=list[RubroInsumo])
def read_rubro_insumos(db: Session = Depends(get_db)):
    rubro_insumos = get_rubro_insumos(db)
    return rubro_insumos

@app.get("/insumo/tipo_erogaciones/", response_model=list[TipoErogacion])
def read_tipo_erogaciones(db: Session = Depends(get_db)):
    tipo_erogaciones = get_tipo_erogaciones(db)
    return tipo_erogaciones