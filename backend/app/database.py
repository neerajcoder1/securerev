from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import time

# Added retry logic for database connection during startup
engine = None
for i in range(5):
    try:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        engine.connect()
        break
    except Exception as e:
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
