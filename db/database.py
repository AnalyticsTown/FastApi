from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///db/data.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://adecoagro:S0m0s3v4@database-1.cumocfjwhkz5.us-east-1.rds.amazonaws.com:5432/base-desarrollo-adecoagro"


#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/prueba'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
