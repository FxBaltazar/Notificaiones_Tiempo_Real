import sqlite3

def obtener_conexion():
    conexion = sqlite3.connect("tienda.db")
    conexion.row_factory = sqlite3.Row
    return conexion
