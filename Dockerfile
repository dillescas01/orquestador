# Usar la imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /programas

# Copiar el archivo requirements.txt para instalar las dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto 8080 para el orquestador
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
