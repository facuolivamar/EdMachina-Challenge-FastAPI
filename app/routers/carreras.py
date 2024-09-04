from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Carreras

router = APIRouter(
    prefix='/carrera',
    tags=['carrera']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class CarreraRequest(BaseModel):
    nombre_carrera: str = Field(min_length=3)

@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Carreras).all()


@router.get("/{carrera_id}", status_code=status.HTTP_200_OK)
async def read_carrera(db: db_dependency, carrera_id: int = Path(gt=0)):
    carrera_model = db.query(Carreras).filter(Carreras.id == carrera_id).first()
    if carrera_model is not None:
        return carrera_model
    raise HTTPException(status_code=404, detail='Carrera not found.')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_carrera(db: db_dependency, carrera_request: CarreraRequest):

    carrera_model = Carreras(**carrera_request.model_dump())

    db.add(carrera_model)
    db.commit()

@router.put("/{carrera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_carrera(db: db_dependency, carrera_request: CarreraRequest, carrera_id: int = Path(gt=0)):
    carrera_model = db.query(Carreras).filter(Carreras.id == carrera_id).first()
    if carrera_model is None:
        raise HTTPException(status_code=404, detail='Carrera not found.')

    carrera_model.nombre_carrera = carrera_request.nombre_carrera

    db.add(carrera_model)
    db.commit()
