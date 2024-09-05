from ..database import Base
from sqlalchemy import Column, Integer, String, Date


class Personas(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True, index=True)
    nombre_persona = Column(String(length=255), nullable=False)
    apellido_persona = Column(String(length=255), nullable=False)
    email_persona = Column(String(length=255), unique=True, nullable=False)
    numero_dni_persona = Column(Integer, unique=True, nullable=False)
    fecha_nacimiento_persona = Column(Date, nullable=True)
