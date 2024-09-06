from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.registros import Registros
from models.materias import Materias
from models.personas import Personas
from models.carreras import Carreras
from schemas.registros import RegistroRequest

# Definimos un router para el manejo de las rutas relacionadas con los "registros"
router = APIRouter(
    prefix='/registro',
    tags=['registro']
)


# Función para obtener una sesión de base de datos"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Definición de la dependencia que inyecta la sesión de la base de datos
db_dependency = Annotated[Session, Depends(get_db)]


# Endpoint para obtener todos los registros
@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Registros).all()


# Endpoint para obtener un registro específico por ID
@router.get("/{registro_id}", status_code=status.HTTP_200_OK)
async def read_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    # Filtra el registro por ID
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id).first()

    # Si se encuentra el registro, lo retorna
    if registro_model is not None:
        return registro_model

    # Si no se encuentra, retorna un error 404
    raise HTTPException(status_code=404, detail='Registro not found.')


# Endpoint para obtener los detalles de un registro, incluyendo relaciones con otras tablas (persona y materia)
@router.get("/detalle/{registro_id}", status_code=status.HTTP_200_OK)
async def read_registro_detalle(db: db_dependency, registro_id: int = Path(gt=0)):
    # Utiliza joinedload para cargar relaciones de persona y materia en la misma consulta
    registro_model = db.query(Registros).options(
        joinedload(Registros.persona),
        joinedload(Registros.materia),
        joinedload(Registros.carrera)
    ).filter(Registros.id == registro_id).first()

    # Si el registro no se encuentra, devuelve un error 404
    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    # Retorna el registro junto con los detalles de las relaciones
    return registro_model


# Endpoint para crear un nuevo registro
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_registro(db: db_dependency,
                          registro_request: RegistroRequest):
    # Creamos una instancia del modelo Registros con los datos recibidos
    registro_model = Registros(**registro_request.model_dump())

    try:
        # Agrega el nuevo registro a la base de datos
        db.add(registro_model)
        db.commit()
        db.refresh(registro_model)
        return registro_model

    except IntegrityError as e:
        db.rollback()  # En caso de error de integridad, se revierte la transacción

        # Verifica si el ID de la materia existe
        materia_id = db.query(Materias).filter(
            Materias.id == registro_request.materia_id
            ).first()
        if materia_id is None:
            raise HTTPException(status_code=422, detail='materia_id does not exist.')

        # Verifica si el ID de la persona existe
        persona_id = db.query(Personas).filter(
            Personas.id == registro_request.persona_id
            ).first()
        if persona_id is None:
            raise HTTPException(status_code=422, detail='persona_id does not exist.')

        # Verifica si el ID de la carrera existe
        carrrera_id = db.query(Carreras).filter(
            Carreras.id == registro_request.carrrera_id
            ).first()
        if carrrera_id is None:
            raise HTTPException(status_code=422, detail='carrera_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint para actualizar un registro existente
@router.put("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_registro(db: db_dependency,
                          registro_request: RegistroRequest,
                          registro_id: int = Path(gt=0)):
    # Busca el registro por ID
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id
        ).first()

    # Si no se encuentra, retorna un error 404
    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    # Actualiza los campos del registro con los datos de la request
    registro_model.calificacion_final = registro_request.calificacion_final
    registro_model.fecha_inicio_cursado = registro_request.fecha_inicio_cursado
    registro_model.fecha_fin_cursado = registro_request.fecha_fin_cursado
    registro_model.activo = registro_request.activo
    registro_model.persona_id = registro_request.persona_id
    registro_model.materia_id = registro_request.materia_id
    registro_model.carrera_id = registro_request.carrera_id

    try:
        db.add(registro_model)
        db.commit()
        return registro_model  # Retorna el registro actualizado

    except IntegrityError as e:
        db.rollback()

        # Validaciones de existencia de IDs de persona y materia, similar a la creación
        materia_id = db.query(Materias).filter(
            Materias.id == registro_request.materia_id
            ).first()
        if materia_id is None:
            raise HTTPException(status_code=422, detail='materia_id does not exist.')

        persona_id = db.query(Personas).filter(
            Personas.id == registro_request.persona_id
            ).first()
        if persona_id is None:
            raise HTTPException(status_code=422, detail='persona_id does not exist.')

        carrrera_id = db.query(Carreras).filter(
            Carreras.id == registro_request.carrrera_id
            ).first()
        if carrrera_id is None:
            raise HTTPException(status_code=422, detail='carrera_id does not exist.')

        raise HTTPException(status_code=422, detail="IntegrityError")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint para eliminar un registro existente
@router.delete("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registro(db: db_dependency, registro_id: int = Path(gt=0)):
    # Busca el registro por ID
    registro_model = db.query(Registros).filter(
        Registros.id == registro_id
        ).first()

    # Si el registro no se encuentra, retorna un error 404
    if registro_model is None:
        raise HTTPException(status_code=404, detail='Registro not found.')

    # Elimina el registro de la base de datos y confirma la transaction
    db.delete(registro_model)
    db.commit()
