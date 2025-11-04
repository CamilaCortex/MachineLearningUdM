# 🐳 Dockerfile para la App de Gatitos
# Imagen base: Python 3.11 slim (ligera)
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="estudiante@mlops.com"
LABEL description="App de gatitos para aprender Docker"

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero (para aprovechar el cache de Docker)
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY app_docker.py app.py
COPY templates/ templates/

# Exponer el puerto 5000 (donde corre Flask)
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
