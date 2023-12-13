from threading import Lock
import csv

# Configuración del bloqueo para la exclusión mutua en la compra de artículos
bloqueo_articulo = Lock()
#***********************************************************************************************************************************
def balanceo_de_carga(nombre_archivo):
    # Leer el inventario de sucursales desde el archivo CSV
    inventario_sucursales = leer_inventario_desde_csv(nombre_archivo)
    
    # Calcula la carga promedio entre todas las sucursales
    carga_promedio = sum(inventario_sucursales) / len(inventario_sucursales)
    
    # Encuentra las sucursales que tienen más carga que la carga promedio
    sucursales_con_exceso = [sucursal for sucursal, carga in enumerate(inventario_sucursales) if carga > carga_promedio]
    
    # Encuentra las sucursales que tienen menos carga que la carga promedio
    sucursales_con_falta = [sucursal for sucursal, carga in enumerate(inventario_sucursales) if carga < carga_promedio]
    
    # Realiza la redistribución de carga
    for sucursal_falta in sucursales_con_falta:
        for sucursal_exceso in sucursales_con_exceso:
            # Transfiere artículos desde sucursales con exceso a sucursales con falta
            transferir_articulos(inventario_sucursales, sucursal_exceso, sucursal_falta)
            
            # Actualiza la carga después de la transferencia
            carga_promedio = sum(inventario_sucursales) / len(inventario_sucursales)
            
            # Vuelve a calcular las sucursales con exceso y falta
            sucursales_con_exceso = [sucursal for sucursal, carga in enumerate(inventario_sucursales) if carga > carga_promedio]
            sucursales_con_falta = [sucursal for sucursal, carga in enumerate(inventario_sucursales) if carga < carga_promedio]

    # Guarda el inventario actualizado en el archivo CSV
    escribir_inventario_a_csv(inventario_sucursales, nombre_archivo)

# Función auxiliar para transferir artículos de una sucursal a otra
def transferir_articulos(inventario_sucursales, sucursal_origen, sucursal_destino):
    # Define la cantidad a transferir (puedes ajustar esto según tu lógica)
    cantidad_a_transferir = 1
    
    # Verifica que la sucursal de origen tenga suficientes artículos para transferir
    if inventario_sucursales[sucursal_origen] >= cantidad_a_transferir:
        # Transfiere la cantidad especificada de artículos
        inventario_sucursales[sucursal_origen] -= cantidad_a_transferir
        inventario_sucursales[sucursal_destino] += cantidad_a_transferir
        print(f"Transferidos {cantidad_a_transferir} artículos de la sucursal {sucursal_origen} a la sucursal {sucursal_destino}.")
    else:
        print(f"No hay suficientes artículos en la sucursal {sucursal_origen} para transferir.")

# Función auxiliar para leer el inventario desde un archivo CSV
def leer_inventario_desde_csv(nombre_archivo):
    inventario_sucursales = []
    with open(nombre_archivo, 'r', newline='') as archivo_csv:
        lector = csv.reader(archivo_csv)
        for fila in lector:
            inventario_sucursales.append(int(fila[1]))  # Suponiendo que la carga está en la segunda columna
    return inventario_sucursales

# Función auxiliar para escribir el inventario a un archivo CSV
def escribir_inventario_a_csv(inventario_sucursales, nombre_archivo):
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        for i, carga in enumerate(inventario_sucursales):
            escritor.writerow([f'Sucursal{i}', carga])  # Puedes ajustar las columnas según tu estructura

#***********************************************************************************************************************************
# Funciones auxiliares
def determinar_sucursal_con_menor_carga(nombre_archivo):
    menor_carga = float('inf')
    sucursal_menor_carga = None

    with open(nombre_archivo, 'r', newline='') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        
        for fila in lector:
            sucursal = fila['Sucursal']
            carga_sucursal = int(fila['Cantidad'])  # Suponiendo que 'Cantidad' es el campo que representa la carga

            if carga_sucursal < menor_carga:
                menor_carga = carga_sucursal
                sucursal_menor_carga = sucursal

    return sucursal_menor_carga

#***********************************************************************************************************************************
def distribuir_articulos(inventario_sucursales, sucursal_destino):
    # Implementa la lógica para distribuir artículos a la sucursal de destino
    pass
#************************************************************************************************************************************
NOMBRE_ARCHIVO_CLIENTES = 'clientes.csv'  # Cambia el nombre según tus necesidades

def consultar_lista_clientes():
    lista_clientes = []

    try:
        with open(NOMBRE_ARCHIVO_CLIENTES, 'r', newline='') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                lista_clientes.append(fila)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta {NOMBRE_ARCHIVO_CLIENTES}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    finally:
        print("Operación de consulta de clientes completada.")

    return lista_clientes

def actualizar_lista_clientes():
    try:
        nuevo_cliente = {
            'id': input("Ingrese el ID del nuevo cliente: "),
            'nombre': input("Ingrese el nombre del nuevo cliente: ")
        }

        with open(NOMBRE_ARCHIVO_CLIENTES, 'a', newline='') as archivo_csv:
            campos = ['id', 'nombre']  # Ajusta los nombres de los campos según tu estructura
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Verifica si el archivo está vacío y escribe los encabezados si es necesario
            if archivo_csv.tell() == 0:
                escritor.writeheader()

            # Escribe el nuevo cliente en el archivo CSV
            escritor.writerow(nuevo_cliente)
    except Exception as e:
        print(f"Error al actualizar la lista de clientes: {e}")
    finally:
        print("Operación de actualización de clientes completada.")

#***********************************************************************************************************************************
def actualizar_lista_clientes(nuevo_cliente):
    with open('lista_clientes.csv', 'a', newline='') as archivo_csv:
        campos = ['id', 'nombre']
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
        escritor.writerow(nuevo_cliente)
#*****************************************************************************************************************************
# Configuración del bloqueo para la exclusión mutua en la compra de artículos
bloqueo_articulo = Lock()

# Función para comprar un artículo y realizar automáticamente la generación de guía y descuento del inventario
def comprar_articulo(id_articulo, id_cliente, serie, inventario_sucursales, nombre_archivo_inventario, nombre_archivo_guias):
    with bloqueo_articulo:
        try:
            # Verifica si hay suficientes existencias en el inventario
            if inventario_sucursales[id_articulo] > 0:
                # Realiza la compra (decrementa las existencias)
                inventario_sucursales[id_articulo] -= 1
                
                # Genera la guía de envío
                guia_envio = f"{id_articulo}-{serie}-{id_cliente}"

                # Almacena la guía de envío en el archivo CSV de guías
                almacenar_guia_envio(guia_envio, nombre_archivo_guias)

                # Registra la transacción en el archivo CSV de transacciones
                registrar_transaccion(id_articulo, id_cliente, nombre_archivo_inventario)

                print(f"Compra realizada correctamente para el IDARTICULO {id_articulo}.")
                print(f"Guía de envío generada y artículo descontado del inventario.")
            else:
                print(f"No hay suficientes existencias para el IDARTICULO {id_articulo}.")
        except Exception as e:
            print(f"Error al realizar compra: {e}")

# Función auxiliar para almacenar la guía de envío en un archivo CSV
def almacenar_guia_envio(guia_envio, nombre_archivo):
    try:
        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            campos = ['GUIA']  # Ajusta los nombres de los campos según tu estructura
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Escribe la guía de envío en el archivo CSV
            escritor.writerow({'GUIA': guia_envio})
    except Exception as e:
        print(f"Error al almacenar guía de envío: {e}")

# Función auxiliar para registrar la transacción en un archivo CSV
def registrar_transaccion(id_articulo, id_cliente, nombre_archivo):
    try:
        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            campos = ['IDARTICULO', 'IDCLIENTE']  # Ajusta los nombres de los campos según tu estructura
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Escribe la transacción en el archivo CSV
            escritor.writerow({'IDARTICULO': id_articulo, 'IDCLIENTE': id_cliente})
    except Exception as e:
        print(f"Error al registrar transacción: {e}")

#****************************************************************************************************************************
# Configuración del bloqueo para la exclusión mutua en la compra de artículos
bloqueo_articulo = Lock()

# Función para generar la guía de envío y descontar del inventario
def generar_guia_y_descontar(id_articulo, serie, id_cliente, inventario_sucursales, nombre_archivo_inventario, nombre_archivo_guias):
    with bloqueo_articulo:
        try:
            # Verifica si hay suficientes existencias en el inventario
            if inventario_sucursales[id_articulo] > 0:
                # Genera la guía de envío
                guia_envio = f"{id_articulo}-{serie}-{id_cliente}"

                # Almacena la guía de envío en el archivo CSV de guías
                almacenar_guia_envio(guia_envio, nombre_archivo_guias)

                # Descontar el artículo del inventario
                inventario_sucursales[id_articulo] -= 1

                # Registra la transacción en el archivo CSV de transacciones
                registrar_transaccion(id_articulo, id_cliente, nombre_archivo_inventario)

                print(f"Guía de envío generada y artículo descontado del inventario correctamente.")
            else:
                print(f"No hay suficientes existencias para el IDARTICULO {id_articulo}.")
        except Exception as e:
            print(f"Error al generar guía de envío y descontar artículo: {e}")

# Función auxiliar para almacenar la guía de envío en un archivo CSV
def almacenar_guia_envio(guia_envio, nombre_archivo):
    try:
        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            campos = ['GUIA']  # Ajusta los nombres de los campos según tu estructura
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Escribe la guía de envío en el archivo CSV
            escritor.writerow({'GUIA': guia_envio})
    except Exception as e:
        print(f"Error al almacenar guía de envío: {e}")

# Función auxiliar para registrar la transacción en un archivo CSV
def registrar_transaccion(id_articulo, id_cliente, nombre_archivo):
    try:
        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            campos = ['IDARTICULO', 'IDCLIENTE']  # Ajusta los nombres de los campos según tu estructura
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Escribe la transacción en el archivo CSV
            escritor.writerow({'IDARTICULO': id_articulo, 'IDCLIENTE': id_cliente})
    except Exception as e:
        print(f"Error al registrar transacción: {e}")

#****************************************************************************************************************************
def main():
    # Ejemplo de uso
    inventario_sucursales = [...]  # Reemplaza con tu propio inventario inicial
    balanceo_de_carga(inventario_sucursales)
    inventario_sucursales = [10, 5, 8]  # Reemplaza con tu propio inventario inicial
    nombre_archivo_inventario = 'inventario.csv'
    nombre_archivo_guias = 'guias_envio.csv'
    generar_guia_y_descontar(0, 'ABC', '456', inventario_sucursales, nombre_archivo_inventario, nombre_archivo_guias)

# Puedes añadir más funciones y lógica según sea necesario
   
if __name__ == "__main__":
    main()
 


