from locust import HttpUser, task, between
import random
import string

class BaseUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    abstract = True  # <-- Mark as abstract

    def on_start(self):
        """Login para obtener token JWT"""
        credentials = self.get_credentials()
        response = self.client.post("/api/login", json=credentials)
        if response.status_code == 200 and "token" in response.json():
            self.token = response.json()["token"]
        else:
            print(f"Error al iniciar sesión: {response.text}")

    def get_headers(self):
        """Encabezados con autenticación"""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def get_credentials(self):
        """Método para sobrescribir en subclases"""
        return {}

# ---- USUARIO ADMIN ----
class AdminUser(BaseUser):
    def get_credentials(self):
        return {"email":"brayan@correo.com","password":"123456"}

    @task(3)
    def listar_usuarios(self):
        self.client.get("/api/users", headers=self.get_headers())

    @task(2)
    def crear_usuario(self):
        new_user = {
            "name": f"UsuarioNuevo{''.join(random.choices(string.ascii_lowercase, k=6))}",
            "email": f"user_{''.join(random.choices(string.ascii_lowercase, k=6))}@test.com",
            "password": "123456",
            "role_id": 2
        }
        self.client.post("/api/users", json=new_user, headers=self.get_headers())

    @task(1)
    def ver_usuario(self):
        response = self.client.get("/api/users", headers=self.get_headers())
        if response.status_code == 200 and response.json():
            usuarios = response.json()
            usuario = random.choice(usuarios)
            self.client.get(f"/api/users/{usuario['id']}", headers=self.get_headers())

    @task(1)
    def actualizar_usuario(self):
        # Primero obtenemos la lista de usuarios para elegir uno al azar
        response = self.client.get("/api/users",headers=self.get_headers())
        if response.status_code == 200 and response.json():
            usuarios = response.json()
            usuario = random.choice(usuarios)
            update_data = {
                "name": f"Usuario Actualizado {random.randint(1, 1000)}",
                "email": f"usuario{random.randint(1, 1000)}@ejemplo.com",
                "password": "newpassword123",
                "role_id": 2
            }
            self.client.put(f"/api/users/{usuario['id']}", json=update_data, headers=self.get_headers())
        
    @task(1)
    def eliminar_usuario(self):
        # Primero obtenemos la lista de usuarios para elegir uno al azar
        response = self.client.get("/api/users",headers=self.get_headers())
        if response.status_code == 200 and response.json():
            usuarios = response.json()
            usuario = random.choice(usuarios)
            self.client.delete(f"/api/users/{usuario['id']}", headers=self.get_headers())

# ---- USUARIO NORMAL ----
class RegularUser(BaseUser):
    def get_credentials(self):
        return {"email": "prueba@correo.com", "password": "123456"}

    @task(3)
    def ver_perfil(self):
        self.client.get("/api/profile", headers=self.get_headers())

    @task(2)
    def actualizar_perfil(self):
        data = {"name": "NuevoNombre"}
        self.client.put("/api/profile", json=data, headers=self.get_headers())
    
    