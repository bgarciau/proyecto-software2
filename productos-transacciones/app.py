from flask import Flask, jsonify, request
import math
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
client=MongoClient("mongodb://localhost:27017/")
db = client ['microservicio']
productos_collection = db["productos"]
transacciones_collection = db["transacciones"]

# Serializador para ObjectId
def serialize_producto(producto):
    return {
        "_id": str(producto["_id"]),
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio": producto["precio"],
        "stock": producto["stock"]
    }

def serialize_transaccion(transaccion):
    return {
        "_id": str(transaccion["_id"]),
        "producto_id": str(transaccion["producto_id"]),
        "usuario_id": transaccion.get("usuario_id"),
        "tipo": transaccion["tipo"],
        "cantidad": transaccion["cantidad"],
        "total": transaccion["total"],
        "estado": transaccion["estado"],
        "fecha": transaccion["fecha"].strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route("/")
def home():
    return jsonify({"mensaje": "Microservicio Productos y transacciones activo"})

###PRODUCTOS###
# CREATE - Crear un producto
@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.get_json()
    if not data.get("nombre") or not data.get("precio") or not data.get("stock"):
        return jsonify({"error": "Debe enviar nombre, precio y stock"}), 400
    
    producto = {
        "nombre": data["nombre"],
        "descripcion": data.get("descripcion", ""),
        "precio": float(data["precio"]),
        "stock": int(data["stock"])
    }
    result = productos_collection.insert_one(producto)
    return jsonify({"mensaje": "Producto creado correctamente", "id": str(result.inserted_id)}), 201

# READ - Listar todos los productos
@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = productos_collection.find()
    return jsonify([serialize_producto(p) for p in productos])

# READ - Obtener un producto por ID
@app.route("/productos/<id>", methods=["GET"])
def obtener_producto(id):
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(serialize_producto(producto))

# UPDATE - Actualizar un producto
@app.route("/productos/<id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.get_json()
    update_data = {}
    if "nombre" in data: update_data["nombre"] = data["nombre"]
    if "descripcion" in data: update_data["descripcion"] = data["descripcion"]
    if "precio" in data: update_data["precio"] = float(data["precio"])
    if "stock" in data: update_data["stock"] = int(data["stock"])

    result = productos_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    return jsonify({"mensaje": "Producto actualizado correctamente"})

# DELETE - Eliminar un producto
@app.route("/productos/<id>", methods=["DELETE"])
def eliminar_producto(id):
    result = productos_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto eliminado correctamente"})

###TRANSACCIONES###

# Crear una transacción (venta o pedido)
@app.route("/transacciones", methods=["POST"])
def crear_transaccion():
    data = request.get_json()
    tipo = data.get("tipo")

    if tipo not in ["venta", "pedido"]:
        return jsonify({"error": "Tipo de transacción inválido. Debe ser venta o pedido."}), 400

    if not data.get("producto_id") or not data.get("cantidad") or not data.get("metodo_pago"):
        return jsonify({"error": "Debe enviar producto_id, cantidad y metodo_pago"}), 400

    producto = productos_collection.find_one({"_id": ObjectId(data["producto_id"])})
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    cantidad = int(data["cantidad"])
    if producto["stock"] < cantidad:
        return jsonify({"error": "Stock insuficiente"}), 400

    # Descuento de stock
    productos_collection.update_one({"_id": producto["_id"]}, {"$inc": {"stock": -cantidad}})

    monto_total = float(producto["precio"]) * cantidad
    direccion_entrega = None

    if tipo == "pedido":
        direccion_entrega = data.get("direccion_entrega")
        if not direccion_entrega:
            return jsonify({"error": "Debe proporcionar una dirección para el pedido"}), 400

    transaccion = {
        "tipo": tipo,
        "usuario_id": data.get("usuario_id"),
        "producto_id": ObjectId(data["producto_id"]),
        "cantidad": cantidad,
        "monto_total": monto_total,
        "direccion_entrega": direccion_entrega,
        "metodo_pago": data["metodo_pago"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    result = transacciones_collection.insert_one(transaccion)
    return jsonify({"mensaje": "Transacción registrada correctamente", "id": str(result.inserted_id)}), 201

# Listar todas las transacciones
@app.route("/transacciones", methods=["GET"])
def listar_transacciones():
    transacciones = transacciones_collection.find()
    return jsonify([serialize_transaccion(t) for t in transacciones])

# Obtener una transacción por ID
@app.route("/transacciones/<id>", methods=["GET"])
def obtener_transaccion(id):
    transaccion = transacciones_collection.find_one({"_id": ObjectId(id)})
    if not transaccion:
        return jsonify({"error": "Transacción no encontrada"}), 404
    return jsonify(serialize_transaccion(transaccion))

# Eliminar una transacción
@app.route("/transacciones/<id>", methods=["DELETE"])
def eliminar_transaccion(id):
    result = transacciones_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Transacción no encontrada"}), 404
    return jsonify({"mensaje": "Transacción eliminada correctamente"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)