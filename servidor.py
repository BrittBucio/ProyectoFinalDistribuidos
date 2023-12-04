import socket
import time
import os
import threading

def send_message_to_server():
    host = '192.168.11.129'  # Cambia 'direccion_ip_maquina_b' por la dirección IP de la máquina B
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Nombre del archivo para almacenar mensajes en la máquina A
    file_a = "mensajes_maquina_a.txt"

    # Comprobar si el archivo ya existe, y si no, crearlo
    if not os.path.exists(file_a):
        with open(file_a, 'w'):
            pass

    # Función para escuchar y mostrar mensajes entrantes desde la máquina B
    def receive_messages():
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Mensaje recibido de máquina B: {message}")

    # Hilo para recibir mensajes desde la máquina B
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()

    while True:
        message = input("Escribe tu mensaje (o 'exit' para salir): ")
        if message == 'exit':
            break

        # Guarda el mensaje en el archivo local
        with open(file_a, 'a') as f:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            message_with_time = f"{current_time}: {message}\n"
            f.write(message_with_time)

        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if _name_ == '_main_':
    send_message_to_server()
