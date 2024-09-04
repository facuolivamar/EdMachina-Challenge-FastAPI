from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Personas
from datetime import date

router = APIRouter(
    prefix='/persona',
    tags=['persona']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class PersonaRequest(BaseModel):
    nombre_persona: str = Field(min_length=1, description="nombre de la Persona")
    apellido_persona: str = Field(min_length=1, description="apellido de la Persona")
    email_persona: str = Field(min_length=3, description="email de la Persona")
    numero_dni_persona: int = Field(gt=0, description="numero de DNI de la Persona")
    anio_nacimiento_persona: date = Field(description="Fecha de Nacimiento de la Persona")


@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Personas).all()


@router.get("/{persona_id}", status_code=status.HTTP_200_OK)
async def read_persona(db: db_dependency, persona_id: int = Path(gt=0)):
    persona_model = db.query(Personas).filter(Personas.id == persona_id).first()
    if persona_model is not None:
        return persona_model
    raise HTTPException(status_code=404, detail='Persona not found.')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_persona(db: db_dependency, persona_request: PersonaRequest):
    persona_model = Personas(**persona_request.model_dump())

    db.add(persona_model)
    db.commit()


@router.put("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_persona(db: db_dependency,
                         persona_request: PersonaRequest,
                         persona_id: int = Path(gt=0)):
    persona_model = db.query(Personas).filter(Personas.id == persona_id).first()
    if persona_model is None:
        raise HTTPException(status_code=404, detail='Persona not found.')

    persona_model.nombre_persona = persona_request.nombre_persona
    persona_model.apellido_persona = persona_request.apellido_persona
    persona_model.email_persona = persona_request.email_persona
    persona_model.numero_dni_persona = persona_request.numero_dni_persona
    persona_model.anio_nacimiento_persona = persona_request.anio_nacimiento_persona

    db.add(persona_model)
    db.commit()


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(db: db_dependency, persona_id: int = Path(gt=0)):
    persona_model = db.query(Personas).filter(Personas.id == persona_id).first()
    if persona_model is None:
        raise HTTPException(status_code=404, detail='Persona not found.')

    db.delete(persona_model)

    db.commit()
