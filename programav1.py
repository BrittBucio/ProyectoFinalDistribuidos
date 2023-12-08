import socket
import threading

def recibir_mensajes(cliente, direccion):
    while True:
        try:
            datos_recibidos = cliente.recv(1024)
            if datos_recibidos:
                print(f"Mensaje recibido de {direccion}: {datos_recibidos.decode('utf-8')}")
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
            mensaje = input()
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
            mensaje = input()
            cliente.sendall(mensaje.encode('utf-8'))

if __name__ == "__main__":
    puerto = int(input("Ingrese el puerto en el que estará conectado: "))

    servidor_hilo = threading.Thread(target=servidor, args=(puerto,))
    servidor_hilo.start()

    while True:
        opcion = input("¿Desea conectar como cliente? (s/n): ")
        if opcion.lower() == 's':
            ip = input("Ingrese la dirección IP a la que desea conectarse: ")
            puerto_cliente = int(input("Ingrese el puerto del servidor al que desea conectarse: "))
            cliente(ip, puerto_cliente)
        elif opcion.lower() == 'n':
            break
