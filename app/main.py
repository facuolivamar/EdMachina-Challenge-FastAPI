from fastapi import FastAPI
from .database import engine, Base
from .routers import carreras, personas, materias, registros

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(carreras.router)
app.include_router(personas.router)
app.include_router(materias.router)
app.include_router(registros.router)
