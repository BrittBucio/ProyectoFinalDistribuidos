import socket
import threading
import time
import os

# Función para manejar la comunicación con un cliente
def handle_client(client_socket, address, messages, file):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        message = f"{current_time} ({address[0]}): {data}"
        messages.append(message)

        # Guardar el mensaje en un archivo
        with open(file, 'a') as f:
            f.write(message + "\n")

        response = f"Mensaje recibido a las {current_time}\n"
        client_socket.send(response.encode('utf-8'))

    client_socket.close()

# Función para enviar mensaje al servidor
def send_message_to_server():
    host = input("Ingrese la dirección IP del servidor: ")  # Ingreso dinámico de la IP del servidor
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Nombre del archivo para almacenar mensajes del cliente
    file_client = "mensajes_cliente.txt"

    # Comprobar si el archivo ya existe, y si no, crearlo
    if not os.path.exists(file_client):
        with open(file_client, 'w'):
            pass

    # Función para escuchar y mostrar mensajes entrantes desde el servidor
    def receive_messages():
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Mensaje recibido del servidor: {message}")

    # Hilo para recibir mensajes desde el servidor
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()

    while True:
        message = input("Escribe tu mensaje (o 'exit' para salir): ")
        if message == 'exit':
            break

        # Guarda el mensaje en el archivo local del cliente
        with open(file_client, 'a') as f:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            message_with_time = f"{current_time}: {message}\n"
            f.write(message_with_time)

        client_socket.send(message.encode('utf-8'))

    client_socket.close()

# Función principal
def main():
    # Ingreso dinámico de la dirección IP del servidor
    server_host = input("Ingrese la dirección IP del servidor: ")
    
    # Iniciar el servidor en un hilo aparte
    server_thread = threading.Thread(target=start_server, args=(server_host,))
    server_thread.start()

    # Ingreso dinámico de las direcciones IP de los clientes
    number_of_clients = int(input("Ingrese la cantidad de clientes a configurar: "))
    client_hosts = []
    for i in range(number_of_clients):
        client_ip = input(f"Ingrese la dirección IP del cliente {i + 1}: ")
        client_hosts.append(client_ip)

    # Iniciar el cliente para enviar mensajes al servidor
    for host in client_hosts:
        client_thread = threading.Thread(target=send_message_to_server, args=(host,))
        client_thread.start()

# Función para iniciar el servidor
def start_server(host):
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Escuchando en {host}:{port}")

    messages = []
    file_server = "mensajes_servidor.txt"  # Nombre del archivo para almacenar mensajes del servidor

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión entrante desde {addr[0]}:{addr[1]}")

        # Iniciar un hilo para manejar la comunicación con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, messages, file_server))
        client_handler.start()

# Ejecución del programa
if __name__ == "__main__":
    main()
