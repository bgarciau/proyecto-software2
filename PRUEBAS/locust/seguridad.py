from locust import HttpUser, task, between
import random
import string


class AuthUser(HttpUser):
    wait_time = between(1, 3)  # Simula el tiempo entre acciones humanas
    @task
    def on_start(self):
        """Se ejecuta al inicio de cada usuario simulado"""
        # Datos aleatorios de usuario
        self.email = f"user_{''.join(random.choices(string.ascii_lowercase, k=6))}@test.com"
        self.password = "12345678"
        self.name = "Usuario de prueba"
        self.token = None

        # Flujo inicial: registro + login
        self.register_user()
        self.login_user()
        self.logout_user()
        self.forgot_password()

    def register_user(self):
        """Registrar un usuario nuevo"""
        payload = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        self.client.post("/api/register", json=payload)

    def login_user(self):
        """Iniciar sesión y obtener token JWT"""
        payload = {
            "email": self.email,
            "password": self.password
        }
        with self.client.post("/api/login", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                self.token = response.json().get("token")
                response.success()
            else:
                response.failure(f"Fallo en login ({response.status_code})")

    def logout_user(self):
        """Cerrar sesión"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            with self.client.post("/api/logout", headers=headers, catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Error al cerrar sesión ({response.status_code})")

    def forgot_password(self):
        """Simula solicitud de recuperación de contraseña"""
        payload = {"email": self.email}
        with self.client.post("/api/forgotpassword", json=payload, catch_response=True) as response:
            if response.status_code in [200, 202]:
                response.success()
            else:
                response.failure(f"Error en recuperación de contraseña ({response.status_code})")