import grpc
import productos_pb2
import productos_pb2_grpc

# Crear canal de comunicación con el servidor gRPC
channel = grpc.insecure_channel('localhost:50051')

# Crear un stub (cliente)
stub = productos_pb2_grpc.ProductosServiceStub(channel)

def create_producto():
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    stock = int(input("Ingrese el stock del producto: "))
    
    request = productos_pb2.Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock
    )
    
    response = stub.CreateProducto(request)  # Llamar al servicio gRPC
    print(f"Producto creado con ID: {response.id}")

def read_producto():
    producto_id = int(input("Ingrese el ID del producto que desea consultar: "))
    request = productos_pb2.ProductoId(id=producto_id)
    response = stub.ReadProducto(request)
    
    if response:
        print(f"Producto encontrado: {response.nombre}, Precio: {response.precio}, Stock: {response.stock}")
    else:
        print("Producto no encontrado.")

def update_producto():
    producto_id = int(input("Ingrese el ID del producto que desea actualizar: "))
    nombre = input("Ingrese el nuevo nombre del producto: ")
    descripcion = input("Ingrese la nueva descripción del producto: ")
    precio = float(input("Ingrese el nuevo precio del producto: "))
    stock = int(input("Ingrese el nuevo stock del producto: "))
    
    request = productos_pb2.Producto(
        id=producto_id,
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock
    )
    
    response = stub.UpdateProducto(request)
    
    if response:
        print(f"Producto actualizado: {response.nombre}, Precio: {response.precio}, Stock: {response.stock}")
    else:
        print("Error al actualizar el producto.")

def delete_producto():
    producto_id = int(input("Ingrese el ID del producto que desea eliminar: "))
    request = productos_pb2.ProductoId(id=producto_id)
    response = stub.DeleteProducto(request)
    
    if response.success:
        print(f"Producto con ID {producto_id} eliminado exitosamente.")
    else:
        print("Error al eliminar el producto.")

# Menú para seleccionar la acción
def menu():
    while True:
        print("\nSeleccione una opción:")
        print("1. Crear producto")
        print("2. Leer producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        
        choice = input("Ingrese el número de la opción: ")
        
        if choice == '1':
            create_producto()
        elif choice == '2':
            read_producto()
        elif choice == '3':
            update_producto()
        elif choice == '4':
            delete_producto()
        elif choice == '5':
            break
        else:
            print("Opción no válida.")

# Ejecutar el menú
menu()
