import socket
import threading

class Nodo:
    def __init__(self, host = '127.0.0.1', puerto = 55555):
        self.nickname = input("Elige un nombre de usuario: ")
        self.nodo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nodo.bind((host, puerto))
        self.nodo.listen()
        self.clientes = []

    def manejar_cliente(self, cliente):
        while True:
            try:
                mensaje = cliente.recv(1024).decode('ascii')
                self.transmitir(mensaje, cliente)
            except:
                index = self.clientes.index(cliente)
                self.clientes.remove(cliente)
                cliente.close()
                print("Cliente desconectado!")
                break

    def transmitir(self, mensaje, cliente):
        for c in self.clientes:
            if c != cliente:
                c.send(mensaje)

    def recibir(self):
        while True:
            cliente, direccion = self.nodo.accept()
            print(f"Conectado con {str(direccion)}")
            self.clientes.append(cliente)
            thread = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            thread.start()

    def escribir(self):
        while True:
            if len(self.clientes) > 0:
                mensaje = f'{self.nickname}: {input("")}'
                for cliente in self.clientes:
                    cliente.send(mensaje.encode('ascii'))

    def iniciar(self):
        thread_recibir = threading.Thread(target=self.recibir)
        thread_recibir.start()

        thread_escribir = threading.Thread(target=self.escribir)
        thread_escribir.start()

nodo = Nodo()
nodo.iniciar()
