from concurrent import futures
import grpc
import productos_pb2_grpc
from productos_service import ProductosService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    productos_pb2_grpc.add_ProductosServiceServicer_to_server(ProductosService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC corriendo en el puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
