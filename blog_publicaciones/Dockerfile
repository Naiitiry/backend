# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos a la imagen
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación en el contenedor
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación Flask (por defecto 5000)
EXPOSE 5000

# Establecer la variable de entorno para Flask
ENV FLASK_APP=run.py

# Ejecutar la aplicación con el comando "flask run"
CMD ["flask", "run", "--host=0.0.0.0"]