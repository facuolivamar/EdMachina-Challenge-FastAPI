from pydantic import BaseModel, Field

# Modelo Pydantic que define la estructura esperada para las requests relacionadas con Carreras
class CarreraRequest(BaseModel):
    nombre_carrera: str = Field(min_length=1, description="Nombre de la Carrera")
