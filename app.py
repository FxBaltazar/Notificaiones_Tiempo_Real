import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from database import obtener_conexion

app = Flask(__name__)
app.secret_key = "clave_secreta_para_carrito_rog"

@app.route('/')
def catalogo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM categorias")
    # Convertir filas a diccionarios manuales para SQLite
    categorias = [dict(row) for row in cursor.fetchall()]
    cursor.execute("SELECT p.*, c.nombre as categoria FROM productos p JOIN categorias c ON p.id_categoria = c.id")
    productos = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return render_template('catalogo.html', categorias=categorias, productos=productos)

@app.route('/agregar/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = {}
    carrito = session['carrito']
    cantidad = int(request.form.get('cantidad', 1))
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad
    session['carrito'] = carrito
    flash("Producto añadido", "success")
    return redirect(url_for('catalogo'))

@app.route('/carrito')
def ver_carrito():
    if 'carrito' not in session or not session['carrito']:
        return render_template('carrito.html', productos=[], total=0)
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    ids = ",".join(session['carrito'].keys())
    cursor.execute(f"SELECT * FROM productos WHERE id IN ({ids})")
    productos_db = [dict(row) for row in cursor.fetchall()]
    productos_carrito = []
    total = 0
    for p in productos_db:
        cant = session['carrito'][str(p['id'])]
        subtotal = p['precio'] * cant
        total += subtotal
        productos_carrito.append({'id': p['id'], 'nombre': p['nombre'], 'precio': p['precio'], 'cantidad': cant, 'subtotal': subtotal})
    cursor.close()
    conexion.close()
    return render_template('carrito.html', productos=productos_carrito, total=total)

@app.route('/vaciar')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('catalogo'))

@app.route('/finalizar', methods=['POST'])
def finalizar_compra():
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    metodo_pago = request.form.get('metodo_pago')
    if 'carrito' not in session or not session['carrito']:
        return redirect(url_for('catalogo'))
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    ids = ",".join(session['carrito'].keys())
    cursor.execute(f"SELECT id, nombre, precio FROM productos WHERE id IN ({ids})")
    productos_db = [dict(row) for row in cursor.fetchall()]
    total = 0
    detalles_insertar = []
    texto_productos_whatsapp = ""
    for p in productos_db:
        cant = session['carrito'][str(p['id'])]
        subtotal = p['precio'] * cant
        total += subtotal
        detalles_insertar.append({'id_producto': p['id'], 'cantidad': cant, 'precio_unitario': p['precio']})
        texto_productos_whatsapp += f"• {cant}x {p['nombre']} (${p['precio']:.2f} c/u)\n"
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cant, p['id']))
    cursor.execute("INSERT INTO ventas (nombre_cliente, telefono_cliente, metodo_pago, total) VALUES (?, ?, ?, ?)", (nombre, telefono, metodo_pago, total))
    id_venta = cursor.lastrowid
    for d in detalles_insertar:
        cursor.execute("INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (?, ?, ?, ?)", (id_venta, d['id_producto'], d['cantidad'], d['precio_unitario']))
    conexion.commit()
    cursor.close()
    conexion.close()
       # ========================================================
    # 4. DISPARAR NOTIFICACIÓN AUTOMÁTICA A WHATSAPP (JSON)
    # ========================================================
    msg = f"🔔 *¡NUEVA VENTA REGISTRADA! (Web)*\n\n"
    msg += f"📄 *Pedido:* #{id_venta}\n"
    msg += f"👤 *Cliente:* {nombre} ({telefono})\n"
    msg += f"💳 *Método de Pago:* {metodo_pago}\n\n"
    msg += f"🛒 *Periféricos Solicitados:*\n{texto_productos_whatsapp}\n"
    msg += f"💰 *Total Neto:* ${total:.2f}\n\n"
    msg += f"⚙️ _Por favor, verifique el abono para preparar el despacho._"

    # Credenciales directas de tu cuenta
    wp_phone = "59169825692"
    wp_token = "r6vrs04yzamxzlpx"
    wp_instance = "instance193038"

    # Cambiamos el endpoint al envío nativo de JSON
    url_api = f"https://api.ultramsg.com/{wp_instance}/messages/chat"

    # Estructura limpia que Render NO va a bloquear
    payload = {
        "token": wp_token,
        "to": wp_phone,
        "body": msg
    }
    
    headers = {'content-type': 'application/json'} # <-- Le avisamos al servidor que va protegido en JSON

    try:
        # Enviamos usando json=payload en vez de data=payload
        requests.post(url_api, json=payload, headers=headers, timeout=12)
    except Exception:
        pass
        
    session.pop('carrito', None)
    return render_template('exito.html', id_venta=id_venta)


if __name__ == '__main__':
    app.run(debug=True)
