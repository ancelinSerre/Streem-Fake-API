from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/streem_sql.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)

# Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   