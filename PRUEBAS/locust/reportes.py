from locust import HttpUser, task, between

class ReportesUser(HttpUser):
    wait_time = between(1, 3)  # Simula el tiempo de espera entre solicitudes

    def on_start(self):
        """Configuración inicial antes de comenzar las tareas"""
        # Simula un token JWT (reemplázalo con uno real si es necesario)
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvYXBpL2xvZ2luIiwiaWF0IjoxNzYwMzMwNjQwLCJleHAiOjE3NjAzMzQyNDAsIm5iZiI6MTc2MDMzMDY0MCwianRpIjoiTWxYS3R3WGhGbGNwbkxUSCIsInN1YiI6IjIiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.e2oeYKeOKhZ51WhKqgx3DA20ZDiKzBgjiQQExuWfgWc"
        self.headers_with_auth = {"Authorization": f"Bearer {self.token}"}

    # ---------------------
    # REPORTES DE USUARIOS
    # ---------------------
    @task(3)
    def reporte_usuarios_pdf(self):
        """Prueba generación de PDF de usuarios"""
        with self.client.get(
            "/reportes/usuarios/pdf",
            headers=self.headers_with_auth,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error PDF usuarios: {response.status_code}")

    @task(2)
    def reporte_usuarios_excel(self):
        """Prueba generación de Excel de usuarios"""
        with self.client.get(
            "/reportes/usuarios/excel",
            headers=self.headers_with_auth,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error Excel usuarios: {response.status_code}")

    # ---------------------
    # REPORTES DE PRODUCTOS
    # ---------------------
    @task(3)
    def reporte_productos_pdf(self):
        """Prueba generación de PDF de productos"""
        with self.client.get(
            "/reportes/productos/pdf", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error PDF productos: {response.status_code}")

    @task(2)
    def reporte_productos_excel(self):
        """Prueba generación de Excel de productos"""
        with self.client.get(
            "/reportes/productos/excel", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error Excel productos: {response.status_code}")

    # -------------------------
    # REPORTES DE TRANSACCIONES
    # -------------------------
    @task(3)
    def reporte_transacciones_pdf(self):
        """Prueba generación de PDF de transacciones"""
        with self.client.get(
            "/reportes/transacciones/pdf", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error PDF transacciones: {response.status_code}")

    @task(2)
    def reporte_transacciones_excel(self):
        """Prueba generación de Excel de transacciones"""
        with self.client.get(
            "/reportes/transacciones/excel", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error Excel transacciones: {response.status_code}")