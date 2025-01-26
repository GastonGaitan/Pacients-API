# Usa una imagen base ligera con Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo requirements.txt primero para aprovechar la cache de Docker
COPY requirements.txt requirements.txt

# Instala las dependencias especificadas en requirements.txt
RUN pip install -r requirements.txt

# Copia el resto de los archivos de tu proyecto al contenedor
COPY . .

# Expone el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
