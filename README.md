# EdMachina Challenge - FastAPI

Este repositorio contiene el proyecto FastAPI desarrollado para el Ed Machina Challenge.

## Tecnologías utilizadas

- **Backend**: FastAPI
- **Base de datos**: PostgreSQL 9.6
- **Frontend**: HTML, CSS, JavaScript
- **ORM**: SQLAlchemy
- **Pydantic**: Requests schemas
- **Migraciones de la base de datos**: Alembic
- **Contenedores**: Docker y Docker Compose
- **Testing**: Postman
- **Diagramación de la base de datos**: PlantUML - DER

## Instalación y ejecución

### 1. Inicialización con Docker

#### Pasos:

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/EdMachina-Challenge-FastAPI.git
   cd EdMachina-Challenge-FastAPI
   ```

2. **Levantar la aplicación con Docker Compose**:

   ```bash
   docker-compose up --build
   ```

3. **Acceder a la aplicación**:

   - **API FastAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Frontend UI**: [http://localhost:4200](http://localhost:4200)

### 2. Inicialización sin Docker

#### Backend (FastAPI):

1. **Instalar las dependencias**:

   Asegúrate de estar en el directorio /app del proyecto y luego ejecuta:

   ```bash
   pipenv shell
   pip install -r requirements.txt
   ```

2. **Configurar PostgreSQL**:

   Configura una base de datos PostgreSQL y actualiza las credenciales en un archivo `.env` con el formato:

   ```bash
   POSTGRES_DB=leadsapp
   POSTGRES_USER=leadsapp
   POSTGRES_PASSWORD=leadsapp
   ```

3. **Levantar el servidor FastAPI**:

   ```bash
   uvicorn main:app --reload --port 8080
   ```

4. **Acceder a la API**: [http://localhost:8080/docs](http://localhost:8080/docs)

#### Frontend:

1. **Navegar al directorio `frontend/`**:

   ```bash
   cd frontend
   ```

2. **Abrir el archivo `index.html` en tu navegador o utilizar un servidor local como `Live Server` en VSCode**.

## Base de datos

### Diagrama de la base de datos

![Diagrama de la Base de Datos](https://github.com/facuolivamar/EdMachina-Challenge-FastAPI/blob/main/docs/diagram_db/diagram_db.png)

### Inserción de datos en la base de datos

Para insertar datos en la base de datos, puedes utilizar el script `inserts.sql` ubicado en el directorio `postgresql_scripts/`:

## Endpoints
### Rutas disponibles:

- **Personas**:
  - `GET /persona`: Obtener todas las personas.
  - `GET /persona/{id}`: Obtener una persona por ID.
  - `POST /persona`: Crear una nueva persona.
  - `PUT /persona/{id}`: Actualizar los datos de una persona.
  - `DELETE /persona/{id}`: Eliminar una persona.

- **Materias**:
  - `GET /materia`: Obtener todas las materias.
  - `GET /materia/{id}`: Obtener una materia por ID.
  - `POST /materia`: Crear una nueva materia.
  - `PUT /materia/{id}`: Actualizar una materia.
  - `DELETE /materia/{id}`: Eliminar una materia.

- **Registros**:
  - `GET /registro`: Obtener todos los registros de cursado.
  - `GET /registro/{id}`: Obtener un registro por ID.
  - `GET /registro/detalle/{id}`: Obtener un registro por ID.
  - `POST /registro`: Crear un nuevo registro de cursado.
  - `PUT /registro/{id}`: Actualizar un registro.
  - `DELETE /registro/{id}`: Eliminar un registro.

- **Carreras**:
  - `GET /carrera`: Obtener todas las carreras.
  - `GET /carrera/{id}`: Obtener una carrera por ID.
  - `POST /carrera`: Crear una nueva carrera.
  - `PUT /carrera/{id}`: Actualizar una carrera.
  - `DELETE /carrera/{id}`: Eliminar una carrera.

## Testing con Postman

Para realizar pruebas de la API, utiliza la colección de Postman proporcionada:

- **Postman Collection**: [Challenge FastAPI - EdMachina](https://www.postman.com/salascuna-system/workspace/challenge-fastapi-edmachina/overview)

### Paquetes principales:

- **FastAPI**: Framework web para el backend.
- **SQLAlchemy**: ORM utilizado para la interacción con la base de datos.
- **Alembic**: Manejo de migraciones de la base de datos.
- **Psycopg2**: Adaptador de PostgreSQL para Python.
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI.

## Licencia

Este proyecto está bajo la licencia MIT. 
