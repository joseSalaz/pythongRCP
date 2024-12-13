import psycopg2
import grpc
import productos_pb2
import productos_pb2_grpc

DATABASE_URL = "postgresql://neondb_owner:IPtn3Zud4RiG@ep-old-brook-a5o96wna.us-east-2.aws.neon.tech/neondb?sslmode=require"

class ProductosService(productos_pb2_grpc.ProductosServiceServicer):
    def CreateProducto(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s) RETURNING id"
            cursor.execute(query, (request.nombre, request.descripcion, request.precio, request.stock))
            producto_id = cursor.fetchone()[0]
            connection.commit()

            return productos_pb2.Producto(
                id=producto_id,
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
                stock=request.stock
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return productos_pb2.Producto()
        finally:
            cursor.close()
            connection.close()

    def ReadProducto(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "SELECT id, nombre, descripcion, precio, stock FROM productos WHERE id = %s"
            cursor.execute(query, (request.id,))
            result = cursor.fetchone()

            if result:
                return productos_pb2.Producto(
                    id=result[0],
                    nombre=result[1],
                    descripcion=result[2],
                    precio=result[3],
                    stock=result[4]
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Producto no encontrado")
                return productos_pb2.Producto()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return productos_pb2.Producto()
        finally:
            cursor.close()
            connection.close()

    def UpdateProducto(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = """
                UPDATE productos 
                SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                WHERE id = %s
            """
            cursor.execute(query, (request.nombre, request.descripcion, request.precio, request.stock, request.id))
            connection.commit()

            if cursor.rowcount > 0:
                return productos_pb2.Producto(
                    id=request.id,
                    nombre=request.nombre,
                    descripcion=request.descripcion,
                    precio=request.precio,
                    stock=request.stock
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Producto no encontrado")
                return productos_pb2.Producto()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return productos_pb2.Producto()
        finally:
            cursor.close()
            connection.close()

    def DeleteProducto(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "DELETE FROM productos WHERE id = %s"
            cursor.execute(query, (request.id,))
            connection.commit()

            if cursor.rowcount > 0:
                return productos_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Producto no encontrado")
                return productos_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return productos_pb2.Empty()
        finally:
            cursor.close()
            connection.close()