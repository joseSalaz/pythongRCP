# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt /app/
COPY server.py /app/
COPY productos_pb2.py /app/
COPY productos_pb2_grpc.py /app/
COPY productos_service.py /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para el servicio gRPC
EXPOSE 50051

# Comando para iniciar el servidor
CMD ["python", "server.py"]
