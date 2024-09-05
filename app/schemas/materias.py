from pydantic import BaseModel, Field


class MateriaRequest(BaseModel):
    nombre_materia: str = Field(min_length=1, description="Nombre de la Materia")
    anio_materia: int = Field(gt=0,
                              description="Año de cursado de la Materia, ejemplo: 5 para 5to año.")
    carrera_id: int = Field(gt=0, description="Carrera relacionada a la Materia")
