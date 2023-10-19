# Usa una imagen base, por ejemplo, Python para aplicaciones Python.
FROM python:3.8

# Establece el directorio de trabajo en el contenedor.
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor.
COPY . /app

# Instala las dependencias.
RUN pip install -r requirements.txt 

# Especifica el comando para ejecutar tu aplicación.
CMD ["python", "main.py"]