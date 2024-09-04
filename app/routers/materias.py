from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Materias

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
    nombre_materia: str = Field(min_length=1)
    anio_materia: int = Field(gt=0)
    carrera_id: int = Field(gt=0)

@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Materias).all()



