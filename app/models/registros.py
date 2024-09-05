from ..database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

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
    
    
    # Relaciones
    persona = relationship("Personas", backref="registros")
    materia = relationship("Materias", backref="registros")
