# Usa una imagen base python 3.11.6-slim-bullseye
FROM python:3.11.6-slim-bullseye

# Instalo las actualizaciones del sistema y Python
RUN apt-get update -y && apt-get install -y python3-pip

#Copio el contenido del directorio actual en el directorio de trabajo del contenedor
COPY . /app

# Establezco el directorio de trabajo
WORKDIR /app

# Instalo las dependencias de Python
RUN pip3 install -r requirements.txt

# Ejecuto mi programa al iniciar el contenedor
CMD ["python3","-i", "index.py"]
