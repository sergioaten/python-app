# Utiliza la imagen de Alpine Linux como base
FROM python:3.9.7-alpine

# Instala las dependencias necesarias
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
# Instala pip y las bibliotecas de Flask y SQLAlchemy
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo srv_bus.py al directorio /srv
COPY *.py /srv/

# Expone el puerto 6901
EXPOSE 6900

# Establece el directorio de trabajo
WORKDIR /srv

# Ejecuta el servidor Flask
CMD ["python", "registro.py"]
