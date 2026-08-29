from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.routers import router
from app.models import Merchant
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureRev API", description="Autonomous Secure Revenue Recovery Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not db.query(Merchant).first():
        m = Merchant(name="Demo Merchant", email="demo@securerev.com", hashed_password=pwd_context.hash("demo"))
        db.add(m)
        db.commit()
    db.close()
