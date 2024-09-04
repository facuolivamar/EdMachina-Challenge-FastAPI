from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Registros
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
    calificacion_final: float = Field(gt=0, le=10)
    fecha_inicio_cursado: date
    fecha_fin_cursado: date
    activo: bool
    persona_id: int
    materia_id: int

@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Registros).all()

@router.get("/{registro_id}", status_code=status.HTTP_200_OK)
async def read_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(Registros.id == registro_id).first()
    if registro_model is not None:
        return registro_model
    raise HTTPException(status_code=404, detail='Registro not found.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_registro(db: db_dependency, registro_request: RegistroRequest):
    registro_model = Registros(**registro_request.model_dump())

    db.add(registro_model)
    db.commit()

@router.put("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_registro(db: db_dependency, registro_request: RegistroRequest, registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(Registros.id == registro_id).first()
    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    registro_model.calificacion_final = registro_request.calificacion_final
    registro_model.fecha_inicio_cursado = registro_request.fecha_inicio_cursado
    registro_model.fecha_fin_cursado = registro_request.fecha_fin_cursado
    registro_model.activo = registro_request.activo
    registro_model.persona_id = registro_request.persona_id
    registro_model.materia_id = registro_request.materia_id

    db.add(registro_model)
    db.commit()

@router.delete("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    registro_model = db.query(Registros).filter(Registros.id == registro_id).first()
    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    db.delete(registro_model)

    db.commit()

