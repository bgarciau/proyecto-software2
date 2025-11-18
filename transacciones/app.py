import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017/"))
db = client['microservicio_transacciones']
transacciones_collection = db["transacciones"]


def serialize_transaccion(transaccion):
    return {
        "_id": str(transaccion["_id"]),
        "tipo": transaccion["tipo"],
        "usuario_id": transaccion["usuario_id"],
        "producto_id": str(transaccion["producto_id"]),
        "cantidad": transaccion["cantidad"],
        "direccion_entrega": transaccion.get("direccion_entrega"),
        "monto_total": transaccion["monto_total"],
        "fecha": transaccion["fecha"]
    }

@app.route("/")
def home():
    return jsonify({"mensaje": "Microservicio transacciones activo"})

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

    cantidad = int(data["cantidad"])
    monto_total = float(data.get("precio", 0)) * cantidad  # El precio debe venir en la petición
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
    app.run(host="0.0.0.0", port=5001, debug=True)
