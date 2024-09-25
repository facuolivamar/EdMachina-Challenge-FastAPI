# Etapa 1: Build de la imagen base con Python 3.12
FROM python:3.12-slim

# Establecer el directorio de trabajo en la imagen
WORKDIR /app

# Copiar el archivo de requisitos desde el directorio raíz
COPY ./requirements.txt /app/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . /app

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
