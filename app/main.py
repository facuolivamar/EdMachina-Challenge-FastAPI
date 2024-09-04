from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import carreras

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(carreras.router)