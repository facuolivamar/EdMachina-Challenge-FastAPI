from database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship


# Definición del modelo Registros que hereda de Base
class Registros(Base):
    __tablename__ = 'registros'

    id = Column(Integer, primary_key=True, index=True)
    calificacion_final = Column(Float, nullable=True)
    fecha_inicio_cursado = Column(Date, nullable=False)
    fecha_fin_cursado = Column(Date, default=None)
    activo = Column(Boolean, default=True)

    materia_id = Column(Integer,
                        ForeignKey("materias.id", ondelete='CASCADE'),
                        nullable=False)
    persona_id = Column(Integer,
                        ForeignKey("personas.id", ondelete='CASCADE'),
                        nullable=False)
    carrera_id = Column(Integer,
                        ForeignKey("carreras.id", ondelete='CASCADE'),
                        nullable=False)

    # Relaciones
    persona = relationship("Personas", backref="registros")  # 1 persona tiene n registros
    materia = relationship("Materias", backref="registros")  # 1 materia tiene n registros
    carrera = relationship("Carreras", backref="registros")  # 1 carrera tiene n registros
