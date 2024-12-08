# Imagen base
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app
COPY ./app /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponer el puerto de la API
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]