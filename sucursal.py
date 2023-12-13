
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

def start_client():
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

def start_server():
    nodos = {
        'A': '192.168.11.134',
        'B': '192.168.11.135',
        'C': '192.168.11.136',
        'D': '192.168.11.137'
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

    #********************************************************************************************************************************
    def ring_algorithm(selected_node):
        # Obtener la lista de nodos en orden de su prioridad para la elección
        nodes_priority_order = ['A', 'B', 'C', 'D']  # Cambia según la lógica de prioridad
    
        # Obtener el índice del nodo actual en la lista
        current_node_index = nodes_priority_order.index(selected_node)
    
        # El nodo actual envía un mensaje de elección al siguiente nodo en el anillo
        next_node_index = (current_node_index + 1) % len(nodes_priority_order)
        next_node = nodes_priority_order[next_node_index]
    
        # Mensaje a enviar al siguiente nodo
        message = "Mensaje de elección"
    
        # Establecer la conexión con el siguiente nodo y enviar el mensaje
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            siguiente_ip = nodos[next_node]  # Obtener la IP del siguiente nodo
            puerto = 12345  # Puerto al que escucha el siguiente nodo
    
            cliente.connect((siguiente_ip, puerto))
            cliente.sendall(message.encode('utf-8'))
    
        print(f"Mensaje enviado al siguiente nodo ({next_node}): {message}")
    #********************************************************************************************************************************

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
    
# Lógica para iniciar el algoritmo del anillo
if __name__ == "__main__":
    selected_node = 'A'  # Nodo actual seleccionado
    ring_algorithm(selected_node)  
    print(f"Nodo maestro: {master_node}")
    slave_nodes = [node for node in nodes_priority_order if node != master_node]
    print(f"Nodos esclavos: {slave_nodes}")
