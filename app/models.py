from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date


class Carreras(Base):
    __tablename__ = 'carreras'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_carrera = Column(String(length=255))

class Personas(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True, index=True)
    nombre_persona = Column(String(length=255))
    apellido_persona = Column(String(length=255))
    email_persona = Column(String, unique=True) 
    numero_dni_persona = Column(Integer)
    anio_nacimiento_persona = Column(Date)
