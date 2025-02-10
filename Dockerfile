# Usa una imagen ligera de Python
FROM python:3.9-slim

# Instalar dependencias del sistema (ej. poppler-utils para pdf2image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar solo requirements.txt primero (para mejor uso de cache)
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear un usuario no root para seguridad
RUN useradd -m appuser
USER appuser

# Exponer el puerto 8000 (si usas Flask/FastAPI)
EXPOSE 8000

# Ejecutar la aplicación
CMD ["python", "WALL-E.py"]