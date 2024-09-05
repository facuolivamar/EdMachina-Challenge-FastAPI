from pydantic import BaseModel, Field


class CarreraRequest(BaseModel):
    nombre_carrera: str = Field(min_length=1, description="Nombre de la Carrera")
