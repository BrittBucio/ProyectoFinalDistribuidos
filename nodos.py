import csv
import socket
import threading
import time
import random
import string

# Nodo maestro inicial
nodo_maestro_actual = 'A'

# Archivo CSV
archivo_csv = 'clientes.csv'

nodos = {
    'A': '192.168.11.128',
    'B': '192.168.11.129',
    'C': '192.168.1.3'
}

def menu(terminar_menu):
    while not terminar_menu.is_set():
        print(f"Bienvenido - Nodo Maestro: {nodo_maestro_actual}")
        print("1. Usuario")
        print("2. Administrador")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_usuario()
        elif opcion == '2':
            menu_administrador()
        elif opcion == '3':
            terminar_menu.set()
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def menu_usuario():
    while True:
        print("\nMenú Usuario:")
        print("1. Consultar productos")
        print("2. Comprar productos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            consultar_productos()
        elif opcion == '2':
            comprar_producto()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def menu_administrador():
    while True:
        print("\nMenú Administrador:")
        print("1. Consultar inventario")
        print("2. Agregar Articulo")
        print("3. Eliminar articulo")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            consultar_inventario()
        elif opcion == '2':
            agregar_articulo()
        elif opcion == '3':
            eliminar_articulo()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def consultar_productos():
    with open(archivo_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        print("\nIDARTICULO | SERIE | SUCURSAL | IDCLIENTE")
        for row in reader:
            id_articulo, serie, sucursal, id_cliente = row
            print(f"{id_articulo} | {serie} | {sucursal} | {id_cliente}")

def comprar_producto():
    id_articulo_a_comprar = input("Ingrese el IDARTICULO del producto a comprar: ")

    # Verificar si el IDARTICULO existe en el archivo CSV
    articulo_existente, id_cliente_actual = verificar_existencia_articulo(id_articulo_a_comprar)

    if not articulo_existente:
        print("El artículo solicitado no existe.")
    elif id_cliente_actual is None:
        # El IDARTICULO no tiene un IDCLIENTE, está disponible
        id_cliente_nuevo = generar_id_cliente_aleatorio()
        print(f"Compra exitosa. Producto disponible para la compra. IDCLIENTE asignado: {id_cliente_nuevo}")
        asignar_cliente_a_articulo(id_articulo_a_comprar, id_cliente_nuevo)
    else:
        # El IDARTICULO ya tiene un IDCLIENTE, no está disponible
        print("El artículo solicitado ya no está disponible.")

def verificar_existencia_articulo(id_articulo):
    with open(archivo_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id_articulo:
                # Se encontró el IDARTICULO, devolver si existe y el IDCLIENTE actual
                return True, row[3]  # True y el IDCLIENTE actual
    # No se encontró el IDARTICULO
    return False, None

def asignar_cliente_a_articulo(id_articulo, id_cliente):
    with open(archivo_csv, 'r', newline='') as file:
        lines = list(csv.reader(file))

    for i, row in enumerate(lines):
        if row[0] == id_articulo:
            # Asignar el IDCLIENTE al IDARTICULO
            lines[i][3] = id_cliente

    with open(archivo_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def generar_id_cliente_aleatorio():
    # Generar un IDCLIENTE aleatorio de 10 caracteres alfanuméricos
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
def consultar_inventario():
    with open(archivo_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        print("\nIDARTICULO | SERIE | SUCURSAL | IDCLIENTE")
        for row in reader:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

def agregar_articulo():
    id_articulo = input("Ingrese el IDARTICULO del nuevo artículo: ")
    serie = input("Ingrese la serie del nuevo artículo: ")
    sucursal = input("Ingrese la sucursal del nuevo artículo: ")
    id_cliente = input("Ingrese el IDCLIENTE del nuevo artículo (deje en blanco si no tiene): ")

    with open(archivo_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        hora_generacion = time.strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([id_articulo, serie, sucursal, id_cliente, hora_generacion])

def eliminar_articulo():
    print("\nEliminar artículo:")
    print("1. Eliminar un solo artículo")
    print("2. Eliminar una serie completa")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        eliminar_articulo_individual()
    elif opcion == '2':
        eliminar_serie_completa()
    else:
        print("Opción no válida. Inténtelo de nuevo.")

def eliminar_articulo_individual():
    id_articulo_a_eliminar = input("Ingrese el IDARTICULO del artículo a eliminar: ")

    with open(archivo_csv, 'r', newline='') as file:
        lines = list(csv.reader(file))

    new_lines = [line for line in lines if line[0] != id_articulo_a_eliminar]

    with open(archivo_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_lines)

def eliminar_serie_completa():
    serie_a_eliminar = input("Ingrese la SERIE de los artículos a eliminar: ")

    with open(archivo_csv, 'r', newline='') as file:
        lines = list(csv.reader(file))

    new_lines = [line for line in lines if line[1] != serie_a_eliminar or line[3] is not None]

    with open(archivo_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_lines)

def manejar_cliente(client_socket, address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Mensaje recibido de {address}: {data.decode()} ({time.strftime('%Y-%m-%d %H:%M:%S')})")
        # Notificar al cliente que el mensaje fue recibido
        client_socket.sendall(b"Mensaje recibido")

    client_socket.close()

def actualizar_nodo_maestro():
    global nodo_maestro_actual
    nodos_en_linea = [nodo for nodo, ip in nodos.items() if verificar_estado(ip)]

    if nodos_en_linea:
        nodo_maestro_actual = nodos_en_linea[0]
        print(f"Nodo Maestro inicial: {nodo_maestro_actual}")

    while True:
        for nodo, ip in nodos.items():
            if verificar_estado(ip):
                nodo_maestro_actual = nodo
                print(f"Nodo Maestro actual: {nodo_maestro_actual}")
                time.sleep(5)  # Esperar antes de volver a verificar
                break

def verificar_estado(ip):
    try:
        with socket.create_connection((ip, 12345), timeout=1):
            pass
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

if name == "main":
    terminar_menu = threading.Event()

    # Configurar el servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    # Iniciar el hilo para el menú
    menu_thread = threading.Thread(target=menu, args=(terminar_menu,))
    menu_thread.start()

    # Iniciar el hilo para la actualización del nodo maestro
    actualizacion_nodo_maestro_thread = threading.Thread(target=actualizar_nodo_maestro)
    actualizacion_nodo_maestro_thread.start()
try:
    while not terminar_menu.is_set():
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=manejar_cliente, args=(client_socket, address))
        client_handler.start()
except KeyboardInterrupt:
    pass
finally:
    # Cerrar el socket del servidor después de salir del bucle principal
    server_socket.close()
