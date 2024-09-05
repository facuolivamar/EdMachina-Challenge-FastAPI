from pydantic import BaseModel, Field
from datetime import date

# Modelo Pydantic que define la estructura esperada para las requests relacionadas con Personas
class PersonaRequest(BaseModel):
    nombre_persona: str = Field(min_length=1,
                                description="Nombre de la Persona")
    apellido_persona: str = Field(min_length=1,
                                  description="Apellido de la Persona")
    email_persona: str = Field(min_length=3,
                               description="Email de la Persona")
    numero_dni_persona: int = Field(gt=0,
                                    description="Numero de DNI de la Persona")
    fecha_nacimiento_persona: date = Field(description="Fecha de Nacimiento de la Persona")
