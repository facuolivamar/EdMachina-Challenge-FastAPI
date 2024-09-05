from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models import Materias, Carreras

router = APIRouter(
    prefix='/materia',
    tags=['materia']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class MateriaRequest(BaseModel):
    nombre_materia: str = Field(min_length=1, description="Nombre de la Materia")
    anio_materia: int = Field(gt=0,
                              description="Año de cursado de la Materia, ejemplo: 5 para 5to año.")
    carrera_id: int = Field(gt=0, description="Carrera relacionada a la Materia")


@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Materias).all()


@router.get("/{materia_id}", status_code=status.HTTP_200_OK)
async def read_materia(db: db_dependency, materia_id: int = Path(gt=0)):
    materia_model = db.query(Materias).filter(Materias.id == materia_id).first()
    if materia_model is not None:
        return materia_model
    raise HTTPException(status_code=404, detail='Materia not found.')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_materia(db: db_dependency, materia_request: MateriaRequest):
    materia_model = Materias(**materia_request.model_dump())

    try:
        db.add(materia_model)
        db.commit()
        return materia_model
    except IntegrityError as e:
        db.rollback()

        carrera_id = db.query(Carreras).filter(
            id == materia_request.carrera_id
            ).first()
        if carrera_id is None:
            raise HTTPException(status_code=422, detail='carrera_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_materia(db: db_dependency,
                         materia_request: MateriaRequest,
                         materia_id: int = Path(gt=0)):
    materia_model = db.query(Materias).filter(Materias.id == materia_id).first()
    if materia_model is None:
        raise HTTPException(status_code=404, detail='Materia not found.')

    materia_model.nombre_materia = materia_request.nombre_materia
    materia_model.anio_materia = materia_request.anio_materia
    materia_model.carrera_id = materia_request.carrera_id

    try:
        db.add(materia_model)
        db.commit()
        return materia_model
    except IntegrityError as e:
        db.rollback()

        carrera_id = db.query(Carreras).filter(
            id == materia_request.carrera_id
            ).first()
        if carrera_id is None:
            raise HTTPException(status_code=422, detail='carrera_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_materia(db: db_dependency, materia_id: int = Path(gt=0)):
    materia_model = db.query(Materias).filter(Materias.id == materia_id).first()
    if materia_model is None:
        raise HTTPException(status_code=404, detail='Materia not found.')

    db.delete(materia_model)

    db.commit()
