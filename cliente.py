import socket
import threading
import time
import io

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

# Función principal
def main():
    host = '0.0.0.0'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Escuchando en {host}:{port}")

    messages = []
    file = "mensajes.txt"  # Nombre del archivo para almacenar mensajes

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión entrante desde {addr[0]}:{addr[1]}")

        # Iniciamos un hilo para manejar la comunicación con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, messages, file))
        client_handler.start()

if _name_ == '_main_':
    main()
