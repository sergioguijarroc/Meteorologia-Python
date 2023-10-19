# Usa una imagen base de Ubuntu
FROM ubuntu:latest

# Instala las actualizaciones del sistema y Python
RUN apt-get update -y && apt-get install -y python3-pip

# Crea un directorio de trabajo en el contenedor
WORKDIR /app

# Copia tu programa y el archivo de requisitos al contenedor
COPY main.py .
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt

# Ejecuta tu programa al iniciar el contenedor
CMD ["python3", "main.py"]
