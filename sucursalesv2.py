import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="root",
    user="root",
    password="debian",
    database="sucursales_bd"
)
cursor = conn.cursor()

# Ejemplo de inserción de datos en la tabla Articulos
def insertar_articulo(nombre, cantidad):
    sql = "INSERT INTO Articulos (nombre, cantidad) VALUES (%s, %s)"
    val = (nombre, cantidad)
    cursor.execute(sql, val)
    conn.commit()

# Ejemplo de consulta de datos en la tabla Articulos
def obtener_articulos():
    cursor.execute("SELECT * FROM Articulos")
    result = cursor.fetchall()
    for row in result:
        print(row)

# Algoritmo de elección de anillo de token (simulado)
def eleccion_anillo_token(lista_nodos):
    # Simulación de elección, podría implementarse según la lógica del anillo de token
    # Aquí solo se imprime el nodo elegido
    print("Nodo maestro elegido:", lista_nodos[0])

# Función principal
def main():
    # Lista de nodos/sucursales disponibles
    lista_nodos = ["Nodo1", "Nodo2", "Nodo3", "Nodo4"]

    # Simulación de elección de nodo maestro utilizando el algoritmo de anillo de token
    eleccion_anillo_token(lista_nodos)

    # Llamar a funciones de inserción y consulta aquí si es necesario
    insertar_articulo("Ejemplo", 10)
    obtener_articulos()

    # Cierra la conexión a la base de datos al finalizar las operaciones
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
