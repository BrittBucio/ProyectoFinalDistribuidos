import socket
import threading

def recibir_mensajes(cliente, direccion, archivo):
    while True:
        try:
            datos_recibidos = cliente.recv(1024)
            if datos_recibidos:
                mensaje = datos_recibidos.decode('utf-8')
                print(f"Mensaje recibido de {direccion}: {mensaje}")
                archivo.write(f"Mensaje recibido de {direccion}: {mensaje}\n")
        except:
            break

def cliente(ip, puerto, archivo):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ip, puerto))
        print(f"Conectado al servidor en {ip}:{puerto}")

        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente, ip, archivo))
        recibir_hilo.start()

        while True:
            mensaje = input()
            cliente.sendall(mensaje.encode('utf-8'))
            archivo.write(f"Mensaje enviado a {ip}:{puerto}: {mensaje}\n")
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
    finally:
        cliente.close()

def servidor(puerto, archivo):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(5)
    print(f"Servidor escuchando en el puerto {puerto}")

    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión entrante desde {direccion}")

        recibir_hilo = threading.Thread(target=recibir_mensajes, args=(cliente, direccion[0], archivo))
        recibir_hilo.start()

        while True:
            mensaje = input()
            cliente.sendall(mensaje.encode('utf-8'))
            archivo.write(f"Mensaje enviado a {direccion[0]}:{puerto}: {mensaje}\n")

if __name__ == "__main__":
    puerto = int(input("Ingrese el puerto en el que estará conectado: "))
    
    # Archivo para guardar la comunicación
    nombre_archivo = f"comunicacion_puerto_{puerto}.txt"
    archivo = open(nombre_archivo, 'a')

    servidor_hilo = threading.Thread(target=servidor, args=(puerto, archivo))
    servidor_hilo.start()

    while True:
        opcion = input("¿Desea conectar como cliente? (s/n): ")
        if opcion.lower() == 's':
            ip = input("Ingrese la dirección IP a la que desea conectarse: ")
            puerto_cliente = int(input("Ingrese el puerto del servidor al que desea conectarse: "))
            cliente(ip, puerto_cliente, archivo)
        elif opcion.lower() == 'n':
            archivo.close()
            break
