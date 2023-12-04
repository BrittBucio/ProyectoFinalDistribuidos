import socket
import threading
import time
import os

def handle_client(client_socket, address, messages, file):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        message = f"{current_time} ({address[0]}): {data}"
        messages.append(message)

        with open(file, 'a') as f:
            f.write(message + "\n")

        response = f"Mensaje recibido a las {current_time}\n"
        client_socket.send(response.encode('utf-8'))

    client_socket.close()

def start_server():
    host = '0.0.0.0'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Escuchando en {host}:{port}")

    messages = []
    file = "mensajes.txt"

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión entrante desde {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, messages, file))
        client_handler.start()

def start_client():
    nodos = {
        'A': '192.168.11.129',
        'B': '192.168.11.130',
        'C': '192.168.11.131',
        'D': '192.168.11.132'
    }

    print("Nodos disponibles:")
    for key, value in nodos.items():
        print(f"{key}: {value}")

    selected_node = input("Elige el nodo al que quieres enviar mensajes: ").upper()

    if selected_node not in nodos:
        print("Opción no válida. Saliendo.")
        return

    host = nodos[selected_node]
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_a = f"mensajes_maquina_{selected_node.lower()}.txt"

    if not os.path.exists(file_a):
        with open(file_a, 'w'):
            pass

    def receive_messages():
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Mensaje recibido del otro nodo ({selected_node}): {message}")

    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()

    while True:
        message = input("Escribe tu mensaje (o 'exit' para salir): ")
        if message == 'exit':
            break

        with open(file_a, 'a') as f:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            message_with_time = f"{current_time}: {message}\n"
            f.write(message_with_time)

        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if name == 'main':
    mode = input("Elige el modo (1 para servidor, 2 para cliente): ")

    if mode == '1':
        start_server()
    elif mode == '2':
        start_client()
    else:
        print("Modo no válido. Ingresa 1 para servidor o 2 para cliente.")
