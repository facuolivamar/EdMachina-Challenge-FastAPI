import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Definir la URL de la base de datos, obteniéndola de las variables de entorno
# Si no está definida, se utiliza una base de datos SQLite por defecto
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL",
    "sqlite:///./app/leadsapp.db"
)

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
