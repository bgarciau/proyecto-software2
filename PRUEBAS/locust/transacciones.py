from locust import HttpUser, task, between
import random

class simpleUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/transacciones")
    
    @task
    def crear_transaccion(self):
        transaccion = {
            "tipo": random.choice(["venta", "pedido"]),
            "usuario_id": 2,  # Simulando IDs de usuario
            "producto_id": "68eb0aa1e44192494859b7c8",  # Simulando IDs de producto
            "cantidad": random.randint(1, 5),
            "monto_total": round(random.uniform(20.0, 500.0), 2),
            "metodo_pago": random.choice(["tarjeta", "nequi", "efectivo"]),
            "direccion_entrega": "Calle Falsa 123",

        }
        self.client.post("/transacciones", json=transaccion)
    
    @task
    def obtener_transaccion(self):
        # Primero obtenemos la lista de transacciones para elegir una al azar
        response = self.client.get("/transacciones")
        if response.status_code == 200 and response.json():
            transacciones = response.json()
            transaccion = random.choice(transacciones)
            self.client.get(f"/transacciones/{transaccion['_id']}")
    
    @task
    def eliminar_transaccion(self):
        # Primero obtenemos la lista de transacciones para elegir una al azar
        response = self.client.get("/transacciones")
        if response.status_code == 200 and response.json():
            transacciones = response.json()
            transaccion = random.choice(transacciones)
            self.client.delete(f"/transacciones/{transaccion['_id']}")
    
