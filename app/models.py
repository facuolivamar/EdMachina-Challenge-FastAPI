from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date


class Carreras(Base):
    __tablename__ = 'carreras'

    id = Column(Integer, primary_key=True, index=True)
    nombre_carrera = Column(String(length=255), nullable=False)


class Personas(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True, index=True)
    nombre_persona = Column(String(length=255), nullable=False)
    apellido_persona = Column(String(length=255), nullable=False)
    email_persona = Column(String(length=255), unique=True, nullable=False)
    numero_dni_persona = Column(Integer, unique=True, nullable=False)
    fecha_nacimiento_persona = Column(Date, nullable=True)


class Materias(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(length=255), nullable=False)
    anio_materia = Column(Integer, nullable=False)
    carrera_id = Column(Integer,
                        ForeignKey("carreras.id", ondelete='CASCADE'),
                        nullable=False)


class Registros(Base):
    __tablename__ = 'registros'

    id = Column(Integer, primary_key=True, index=True)
    calificacion_final = Column(Float, nullable=False)
    fecha_inicio_cursado = Column(Date, nullable=False)
    fecha_fin_cursado = Column(Date, default=None)
    activo = Column(Boolean, default=True)

    materia_id = Column(Integer,
                        ForeignKey("materias.id", ondelete='CASCADE'),
                        nullable=False)
    persona_id = Column(Integer,
                        ForeignKey("personas.id", ondelete='CASCADE'),
                        nullable=False)
