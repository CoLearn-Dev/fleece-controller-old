from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./state.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=16,
    max_overflow=64,
    isolation_level="READ UNCOMMITTED",
    connect_args={"check_same_thread": False},  # arg for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
