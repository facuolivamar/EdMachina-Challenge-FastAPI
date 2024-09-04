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

class Materias(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(length=255))
    anio_materia= Column(Integer)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))

class Registros(Base):
    __tablename__ = 'registros'

    id = Column(Integer, primary_key=True, index=True)
    calificacion_final = Column(Float)
    fecha_inicio_cursado = Column(Date)
    fecha_fin_cursado = Column(Date, default=None)
    activo = Column(Boolean, default=True)

    materia_id = Column(Integer, ForeignKey("materias.id"))
    persona_id = Column(Integer, ForeignKey("personas.id"))
