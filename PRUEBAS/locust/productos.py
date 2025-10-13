from locust import HttpUser, task, between
import random

class simpleUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/productos")
    
    @task
    def crear_producto(self):
        producto = {
            "nombre": f"Producto {random.randint(1, 1000)}",
            "descripcion": "Descripción de prueba",
            "precio": round(random.uniform(10.0, 100.0), 2),
            "stock": random.randint(1, 50)
        }
        self.client.post("/productos", json=producto)
    
    @task
    def obtener_producto(self):
        # Primero obtenemos la lista de productos para elegir uno al azar
        response = self.client.get("/productos")
        if response.status_code == 200 and response.json():
            productos = response.json()
            producto = random.choice(productos)
            self.client.get(f"/productos/{producto['_id']}")
    
    @task
    def actualizar_producto(self):
        # Primero obtenemos la lista de productos para elegir uno al azar
        response = self.client.get("/productos")
        if response.status_code == 200 and response.json():
            productos = response.json()
            producto = random.choice(productos)
            update_data = {
                "nombre": f"Producto Actualizado {random.randint(1, 1000)}",
                "precio": round(random.uniform(10.0, 100.0), 2),
                "stock": random.randint(1, 50)
            }
            self.client.put(f"/productos/{producto['_id']}", json=update_data)

    @task
    def eliminar_producto(self):
        # Primero obtenemos la lista de productos para elegir uno al azar
        response = self.client.get("/productos")
        if response.status_code == 200 and response.json():
            productos = response.json()
            producto = random.choice(productos)
            self.client.delete(f"/productos/{producto['_id']}")