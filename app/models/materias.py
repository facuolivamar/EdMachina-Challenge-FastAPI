from database import Base
from sqlalchemy import Column, Integer, String


class Materias(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(length=255), nullable=False)
    anio_materia = Column(Integer, nullable=False)
