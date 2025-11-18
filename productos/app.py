from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "microservicio")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# AHORA SÍ DEFINIMOS LA COLECCIÓN
productos_collection = db["productos"]

# Serializador
def serialize_producto(producto):
    return {
        "_id": str(producto["_id"]),
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio": producto["precio"],
        "stock": producto["stock"]
    }

@app.route("/")
def home():
    return jsonify({"mensaje": "Microservicio Productos activo"})

### CRUD ###
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
    return jsonify({
        "mensaje": "Producto creado correctamente",
        "id": str(result.inserted_id),
        "nombre": producto["nombre"]
    }), 201


@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = productos_collection.find()
    return jsonify([serialize_producto(p) for p in productos])


@app.route("/productos/<id>", methods=["GET"])
def obtener_producto(id):
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(serialize_producto(producto))


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


@app.route("/productos/<id>", methods=["DELETE"])
def eliminar_producto(id):
    result = productos_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto eliminado correctamente"})


if __name__ == "__main__":
    # MUY IMPORTANTE
    app.run(host="0.0.0.0", port=5000)
