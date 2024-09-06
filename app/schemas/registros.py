from pydantic import BaseModel, Field
from datetime import date


# Modelo Pydantic que define la estructura esperada para las requests relacionadas con Registros
class RegistroRequest(BaseModel):
    calificacion_final: float | None = Field(
        gt=0,
        le=10,
        description="Calificacion final del Alumno"
    )
    fecha_inicio_cursado: date = Field(
        description="Fecha de Inicio de Cursado de la Materia"
    )
    fecha_fin_cursado: date | None = Field(
        description="Fecha de finalizacion del Cursado de la Materia"
    )
    activo: bool | None = Field(
        description="Estado del Alumno"
    )
    persona_id: int = Field(
        gt=0,
        description="Persona relacionada al Registro"
    )
    materia_id: int = Field(
        gt=0,
        description="Materia relacionada al Registro"
    )
    carrera_id: int = Field(
        gt=0,
        description="Carrera relacionada al Registro"
    )
