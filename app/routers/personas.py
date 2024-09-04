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
    nombre_persona: str = Field(min_length=1)
    apellido_persona: str = Field(min_length=1)
    email_persona: str = Field(min_length=3) 
    numero_dni_persona: int = Field(gt=0)
    anio_nacimiento_persona: date

@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Personas).all()

@router.get("/{persona_id}", status_code=status.HTTP_200_OK)
async def read_persona(db: db_dependency, persona_id: int = Path(gt=0)):
    persona_model = db.query(Personas).filter(Personas.id == persona_id).first()
    if persona_model is not None:
        return persona_model
    raise HTTPException(status_code=404, detail='Persona not found.')

