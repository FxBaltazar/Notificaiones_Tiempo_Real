import sqlite3

conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, id_categoria INTEGER NOT NULL, nombre TEXT NOT NULL, descripcion TEXT, precio REAL NOT NULL, stock INTEGER NOT NULL, imagen TEXT);
CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre_cliente TEXT NOT NULL, telefono_cliente TEXT NOT NULL, metodo_pago TEXT NOT NULL, total REAL NOT NULL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS detalle_ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, id_venta INTEGER NOT NULL, id_producto INTEGER NOT NULL, cantidad INTEGER NOT NULL, precio_unitario REAL NOT NULL);

INSERT OR IGNORE INTO categorias (id, nombre) VALUES (1, 'Teclados'), (2, 'Mouses'), (3, 'Audio'), (4, 'Conectividad');

INSERT OR IGNORE INTO productos (id, id_categoria, nombre, descripcion, precio, stock, imagen) VALUES
(1, 1, 'ASUS ROG Strix Flare II Animate', 'Teclado mecánico gamer premium, switches ROG NX Red.', 220.00, 10, 'rog_flare_ii.jpg'),
(2, 1, 'ASUS ROG Scope RX TKL Wireless', 'Teclado gamer compacto 80%, switches ópticos ROG RX.', 140.00, 15, 'rog_scope_rx.jpg'),
(3, 1, 'ASUS Marshmallow KW100', 'Teclado inalámbrico de oficina ultra delgado y silencioso.', 45.00, 20, 'asus_marshmallow.jpg'),
(4, 2, 'ASUS ROG Spatha X Wireless', 'Mouse gamer premium inalámbrico, 19000 DPI, 12 botones.', 150.00, 8, 'rog_spatha_x.jpg'),
(5, 2, 'ASUS ROG Keris Wireless AimPoint', 'Mouse gamer ergonómico ultraligero (75g), sensor 36000 DPI.', 90.00, 12, 'rog_keris.jpg'),
(6, 2, 'ASUS WT300 Wireless', 'Mouse inalámbrico de oficina ergonómico básico.', 20.00, 25, 'asus_wt300.jpg'),
(7, 3, 'ASUS ROG Carnyx', 'Micrófono gamer de condensador USB profesional.', 180.00, 5, 'rog_carnyx.jpg'),
(8, 3, 'ASUS ROG Strix Magnus', 'Micrófono gamer para streaming compacto con cancelación ambiental.', 130.00, 7, 'rog_magnus.jpg'),
(9, 3, 'ASUS ROG Theta 7.1 Type-C', 'Audífonos gamer premium con sonido envolvente 7.1 real.', 290.00, 6, 'rog_theta.jpg'),
(10, 3, 'ASUS ROG Delta Core', 'Audífonos gamer estándar, audio de alta resolución.', 85.00, 14, 'rog_delta_core.jpg'),
(11, 4, 'ASUS ROG Rapture GT6 (Single)', 'Router gamer Wi-Fi 6 de malla tribanda, alta velocidad.', 260.00, 4, 'rog_rapture_gt6.jpg'),
(12, 4, 'ASUS RT-AX53U Dual Band', 'Router estándar Wi-Fi 6 para el hogar, velocidades Gigabit.', 65.00, 18, 'asus_rt_ax53u.jpg'),
(13, 4, 'TP-Link USB 3.0 Hub 4 Ports', 'Hub económico con cuerpo de plástico resistente.', 15.00, 30, 'tplink_4ports.jpg'),
(14, 4, 'TP-Link UH700 Premium Hub', 'Hub USB 3.0 premium de 7 puertos con interruptores.', 40.00, 10, 'tplink_uh700.jpg');
""")
conexion.commit()
conexion.close()
print("¡Base de datos SQLite preparada!")
