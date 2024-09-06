import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno definidas en Docker
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("DB_SERVER")
DB_NAME = os.environ.get("POSTGRES_DB")

# Definir la URL de la base de datos PostgreSQL si las variables están presentes
if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
else:
    # Si alguna variable no está definida, se utiliza SQLite por defecto
    SQLALCHEMY_DATABASE_URL = "sqlite:///./leadsapp.db"

try:
    # Crear el engine de SQLAlchemy, que se encargará de gestionar la conexión con la base de datos
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Crear una sesión local con SQLAlchemy, la cual es necesaria para interactuar con la base de datos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Declarar la clase base para definir los modelos (tablas) en la base de datos
    Base = declarative_base()

except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")
except Exception as e:
    print(f"Error: {e}")
