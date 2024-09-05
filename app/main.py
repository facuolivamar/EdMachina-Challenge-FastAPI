from fastapi import FastAPI
from .database import engine, Base
from .routers import carreras, personas, materias, registros

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Crear las tablas en la base de datos usando SQLAlchemy y el engine conectado
# Si las tablas ya existen, no se modifican
Base.metadata.create_all(bind=engine)


# Ruta para verificar el estado del servidor
# Devuelve un mensaje indicando que la API está en funcionamiento
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


# Incluir los routers de las diferentes entidades (carreras, personas, materias, registros)
# Estos routers contienen las rutas específicas para cada entidad
app.include_router(carreras.router)
app.include_router(personas.router)
app.include_router(materias.router)
app.include_router(registros.router)
