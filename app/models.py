from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date


class Carreras(Base):
    __tablename__ = 'carreras'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_carrera = Column(String(length=255))
