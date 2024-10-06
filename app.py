import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL de los otros microservicios
PRODUCTOS_URL = "http://productos:8000/productos"
PEDIDOS_URL = "http://pedidos:8001/pedidos"

# Ruta para el orquestador, donde se manejará la creación de pedidos
@app.route('/orquestador/pedido', methods=['POST'])
def crear_pedido():
    data = request.json
    cliente = data.get('cliente')
    detalles = data.get('detalles')

    # Paso 1: Verificar inventario en el microservicio de productos
    for detalle in detalles:
        producto_id = detalle['producto_id']
        cantidad = detalle['cantidad']

        # Hacemos la solicitud al microservicio de productos para obtener el inventario
        producto_response = requests.get(f"{PRODUCTOS_URL}/{producto_id}")
        if producto_response.status_code != 200:
            return jsonify({"error": f"Error al obtener el producto ID {producto_id}"}), 400

        producto_data = producto_response.json()
        if producto_data['inventario'] < cantidad:
            return jsonify({"error": f"Inventario insuficiente para el producto ID {producto_id}"}), 400

    # Paso 2: Crear el pedido en el microservicio de pedidos
    pedido_data = {
        "cliente": cliente,
        "detalles": detalles
    }
    pedido_response = requests.post(PEDIDOS_URL, json=pedido_data)
    if pedido_response.status_code != 201:
        return jsonify({"error": "Error al crear el pedido"}), 500

    # Paso 3: Actualizar el inventario en el microservicio de productos
    for detalle in detalles:
        producto_id = detalle['producto_id']
        cantidad = detalle['cantidad']

        # Hacemos la solicitud al microservicio de productos para actualizar el inventario
        update_response = requests.post(f"{PRODUCTOS_URL}/{producto_id}/actualizar_inventario", json={"cantidad": cantidad})
        if update_response.status_code != 200:
            return jsonify({"error": f"Error al actualizar el inventario del producto ID {producto_id}"}), 500

    return jsonify({"message": "Pedido creado y el inventario actualizado con éxito"}), 201

# Echo test para verificar que el orquestador está funcionando
@app.route('/')
def echo_test():
    return jsonify({"message": "Orquestador funcionando correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
