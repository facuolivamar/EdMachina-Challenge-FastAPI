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

