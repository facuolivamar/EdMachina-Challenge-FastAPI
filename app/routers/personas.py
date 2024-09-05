from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.personas import Personas
from ..schemas.personas import PersonaRequest

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

    try:
        db.add(persona_model)
        db.commit()
        return persona_model
    except IntegrityError as e:
        db.rollback()

        email_personas = db.query(Personas).filter(
            Personas.email_persona == persona_request.email_persona
            ).first()
        if email_personas is not None:
            raise HTTPException(status_code=422, detail='email already exists.')

        numero_dni_personas = db.query(Personas).filter(
            Personas.numero_dni_persona == persona_request.numero_dni_persona
            ).first()
        if numero_dni_personas is not None:
            raise HTTPException(status_code=422, detail='numero_dni_persona already exists.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


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
    persona_model.fecha_nacimiento_persona = persona_request.fecha_nacimiento_persona

    try:
        db.add(persona_model)
        db.commit()
        return persona_model
    except IntegrityError as e:
        db.rollback()

        email_personas = db.query(Personas).filter(
            Personas.email_persona == persona_request.email_persona
            ).first()
        if email_personas is not None and email_personas.id != persona_id:
            raise HTTPException(status_code=422, detail='email already exists.')

        numero_dni_personas = db.query(Personas).filter(
            Personas.numero_dni_persona == persona_request.numero_dni_persona
            ).first()
        if numero_dni_personas is not None and numero_dni_personas.id != persona_id:
            raise HTTPException(status_code=422, detail='numero_dni_persona already exists.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(db: db_dependency, persona_id: int = Path(gt=0)):
    persona_model = db.query(Personas).filter(Personas.id == persona_id).first()
    if persona_model is None:
        raise HTTPException(status_code=404, detail='Persona not found.')

    db.delete(persona_model)

    db.commit()
