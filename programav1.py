import socket
import threading

def recibir_mensajes(cliente, direccion):
    while True:
        try:
            datos_recibidos = cliente.recv(1024)
            if datos_recibidos:
                mensaje = datos_recibidos.decode('utf-8')
                print(f"Mensaje recibido de {direccion}: {mensaje}")
        except:
            break

def cliente(ip, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ip, puerto))
        print(f"Conectado al servidor en {ip}:{puerto}")

        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente, ip))
        recibir_hilo.start()

        while True:
            mensaje = input("Mensaje para enviar al servidor: ")
            cliente.sendall(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
    finally:
        cliente.close()

def servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(5)
    print(f"Servidor escuchando en el puerto {puerto}")

    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión entrante desde {direccion}")

        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente, direccion[0]))
        recibir_hilo.start()

        while True:
            mensaje = input("Mensaje para enviar al cliente: ")
            cliente.sendall(mensaje.encode('utf-8'))

if __name__ == "__main__":
    puerto = int(input("Ingrese el puerto en el que estará conectado: "))

    servidor_hilo = threading.Thread(target=servidor, args=(puerto,))
    servidor_hilo.start()

    cliente_hilo = threading.Thread(target=cliente, args=('127.0.0.1', puerto))
    cliente_hilo.start()
