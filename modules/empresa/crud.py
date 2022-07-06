from sqlalchemy.orm import Session

from modules.empresa import models, schemas


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
                             --sql
                            SELECT 
                            empresas.id, 
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
                            monedas.detalle_moneda AS detalle_moneda_primaria, 
                            monedas1.detalle_moneda AS detalle_moneda_secundaria, 
                            detalle_rubro_empresa
                            FROM empresas
                            LEFT JOIN cond_ivas ON cond_ivas.id = empresas.cond_iva_id
                            LEFT JOIN monedas ON monedas.id = empresas.moneda_primaria_id
                            LEFT JOIN monedas AS monedas1 ON monedas1.id = empresas.moneda_secundaria_id
                            LEFT JOIN rubro_empresas ON rubro_empresas.id = empresas.rubro_empresa_id;
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


