from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models import Registros, Materias, Personas
from datetime import date

router = APIRouter(
    prefix='/registro',
    tags=['registro']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class RegistroRequest(BaseModel):
    calificacion_final: float = Field(gt=0, le=10, description="Calificacion final del Alumno")
    fecha_inicio_cursado: date = Field(description="Fecha de Inicio de Cursado de la Materia")
    fecha_fin_cursado: date | None = Field(description="Fecha de finalizacion del Cursado de la Materia")
    activo: bool | None = Field(description="Estado del Alumno")
    persona_id: int = Field(gt=0, description="Persona relacionada al Registro")
    materia_id: int = Field(gt=0, description="Materia relacionada al Registro")


@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Registros).all()


@router.get("/{registro_id}", status_code=status.HTTP_200_OK)
async def read_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id).first()

    if registro_model is not None:
        return registro_model
    raise HTTPException(status_code=404, detail='Registro not found.')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_registro(db: db_dependency,
                          registro_request: RegistroRequest):
    registro_model = Registros(**registro_request.model_dump())

    try:
        db.add(registro_model)
        db.commit()
        return registro_model
    except IntegrityError as e:
        db.rollback()

        materia_id = db.query(Materias).filter(
            Materias.id == registro_request.materia_id
            ).first()
        if materia_id is None:
            raise HTTPException(status_code=422, detail='materia_id does not exist.')

        persona_id = db.query(Personas).filter(
            Personas.id == registro_request.persona_id
            ).first()
        if persona_id is None:
            raise HTTPException(status_code=422, detail='persona_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_registro(db: db_dependency,
                          registro_request: RegistroRequest,
                          registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id
        ).first()

    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    registro_model.calificacion_final = registro_request.calificacion_final
    registro_model.fecha_inicio_cursado = registro_request.fecha_inicio_cursado
    registro_model.fecha_fin_cursado = registro_request.fecha_fin_cursado
    registro_model.activo = registro_request.activo
    registro_model.persona_id = registro_request.persona_id
    registro_model.materia_id = registro_request.materia_id

    try:
        db.add(registro_model)
        db.commit()
        return registro_model
    except IntegrityError as e:
        db.rollback()

        materia_id = db.query(Materias).filter(
            Materias.id == registro_request.materia_id
            ).first()
        if materia_id is None:
            raise HTTPException(status_code=422, detail='materia_id does not exist.')

        persona_id = db.query(Personas).filter(
            Personas.id == registro_request.persona_id
            ).first()
        if persona_id is None:
            raise HTTPException(status_code=422, detail='persona_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id
        ).first()

    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    db.delete(registro_model)

    db.commit()
