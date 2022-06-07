from sqlalchemy.orm import Session

from empresa import models, schemas


def get_rubro_empresas(db: Session):
    return db.query(models.Alta_rubro_empresa_modelo).all()


def get_monedas(db: Session):
    return db.query(models.Alta_moneda_modelo).all()


def get_cond_ivas(db: Session):
    return db.query(models.Alta_cond_IVA_modelo).all()

# def get_empresas(db: Session):
#     return db.query(models.Alta_empresa_modelo).all()


def get_empresas(db: Session):
    statement = """
                            select empresas.id, 
                            activo, 
                            razon_social, 
                            direccion_calle, 
                            direccion_nro, 
                            direccion_localidad, 
                            direccion_provincia,
                            direccion_pais, 
                            direccion_cod_postal, 
                            cuit, 
                            fecha_cierre, 
                            detalle_cond_iva,
                            tipo_metodo_valorizacion, 
                            monedas.detalle_moneda as detalle_moneda_primaria, 
                            monedas1.detalle_moneda as detalle_moneda_secundaria, 
                            detalle_rubro_empresa
                            from empresas
                            left join cond_ivas on cond_ivas.id = empresas.cond_iva_id
                            left join monedas on monedas.id = empresas.moneda_primaria_id
                            left join monedas as monedas1 on monedas1.id = empresas.moneda_secundaria_id
                            left join rubro_empresas on rubro_empresas.id = empresas.rubro_empresa_id
    """

    return db.execute(statement).all()


def get_empresa(db: Session, razon: str, pais: str):
    return db.query(models.Alta_empresa_modelo).filter(models.Alta_empresa_modelo.razon_social == razon).filter(models.Alta_empresa_modelo.direccion_pais == pais).first()


def drop_empresas(db: Session):
    db.query(models.Alta_empresa_modelo).delete()
    db.commit()


def create_empresa(db: Session, empresa: schemas.EmpresaBase):
    db_empresa = models.Alta_empresa_modelo(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


def elegir_metodo_valuacion():
    ""
