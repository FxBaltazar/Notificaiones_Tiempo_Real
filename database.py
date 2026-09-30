import mysql.connector

def obtener_conexion():
    """Establece la conexión con la base de datos de XAMPP"""
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Usuario por defecto de XAMPP
        password="",        # Contraseña por defecto de XAMPP (vacía)
        database="tienda_perifericos"
    )
