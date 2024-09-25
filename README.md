# EdMachina Challenge - FastAPI

This repository contains the FastAPI project developed for the **EdMachina Challenge**.

## Technologies Used

- **Backend**: FastAPI, Python
- **Database**: PostgreSQL 9.6
- **Frontend**: React, Ant Design, Axios, Node.js, TypeScript
- **ORM**: SQLAlchemy
- **Request Schemas**: Pydantic
- **Database Migrations**: Alembic
- **Containers**: Docker and Docker Compose
- **Testing**: Postman
- **Database Diagram**: PlantUML (ERD)

## Installation and Execution

### 1. Initialization with Docker

#### Steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/EdMachina-Challenge-FastAPI.git
   cd EdMachina-Challenge-FastAPI
   ```

2. **Start the application with Docker Compose**:

   ```bash
   docker-compose up --build
   ```

3. **Access the application**:

   - **FastAPI API**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Frontend UI**: [http://localhost:3000](http://localhost:3000)

### 2. Initialization without Docker

#### Backend (FastAPI):

1. **Install dependencies**:

   Ensure you are in the `/app` directory of the project, then run:

   ```bash
   pipenv shell
   pip install -r requirements.txt
   ```

2. **Configure PostgreSQL**:

   Set up a PostgreSQL database and update the credentials in a `.env` file with the following format:

   ```bash
   POSTGRES_DB=your_postgress_db
   POSTGRES_USER=your_postgress_user
   POSTGRES_PASSWORD=your_postgress_app
   DB_HOST=your_postgress_host
   ```

3. **Start the FastAPI server**:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Access the API**: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Frontend:

1. **Navigate to the `frontend/` directory**:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start the React frontend**:

   ```bash
   npm start
   ```

4. **Access the Frontend UI**: [http://localhost:3000](http://localhost:3000)

## Database

### Database Diagram

![Database Diagram](https://github.com/facuolivamar/EdMachina-Challenge-FastAPI/blob/main/docs/diagram_db/diagram_db.png)

### Inserting Data into the Database

To insert data into the database, you can use the `inserts.sql` script located in the `postgresql_scripts/` directory.

## Endpoints

### Available Routes:

- **Personas**:
  - `GET /persona`: Retrieve all personas.
  - `GET /persona/{id}`: Retrieve a persona by ID.
  - `POST /persona`: Create a new persona.
  - `PUT /persona/{id}`: Update a persona's information.
  - `DELETE /persona/{id}`: Delete a persona.

- **Materias**:
  - `GET /materia`: Retrieve all materias.
  - `GET /materia/{id}`: Retrieve a materia by ID.
  - `POST /materia`: Create a new materia.
  - `PUT /materia/{id}`: Update a materia's information.
  - `DELETE /materia/{id}`: Delete a materia.

- **Registros**:
  - `GET /registro`: Retrieve all registros.
  - `GET /registro/{id}`: Retrieve a registro by ID.
  - `GET /registro/detalle/{id}`: Retrieve detailed information about a registro by ID.
  - `POST /registro`: Create a new registro.
  - `PUT /registro/{id}`: Update a registro's information.
  - `DELETE /registro/{id}`: Delete a registro.

- **Carreras**:
  - `GET /carrera`: Retrieve all carreras.
  - `GET /carrera/{id}`: Retrieve a carrera by ID.
  - `POST /carrera`: Create a new carrera.
  - `PUT /carrera/{id}`: Update a carrera's information.
  - `DELETE /carrera/{id}`: Delete a carrera.

## Testing with Postman

To test the API, use the provided Postman collection:

- **Postman Collection**: [Challenge FastAPI - EdMachina](https://www.postman.com/salascuna-system/workspace/challenge-fastapi-edmachina/overview)

### Main Packages:

- **FastAPI**: Web framework for the backend.
- **SQLAlchemy**: ORM used to interact with the database.
- **Alembic**: Database migration tool.
- **Psycopg2**: PostgreSQL adapter for Python.
- **Uvicorn**: ASGI server for running FastAPI.

## License

This project is licensed under the MIT License. 
