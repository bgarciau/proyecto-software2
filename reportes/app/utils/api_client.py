import httpx

# URLs de tus otros microservicios (ajusta los puertos y rutas según tu entorno)
LARAVEL_API_URL = "http://localhost:8000/api"  # usuarios
FLASK_API_URL = "http://localhost:5000"    # productos y transacciones


async def get_usuarios(token: str):
    print("🔍 Token recibido en get_usuarios:", token)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(f"{LARAVEL_API_URL}/users", headers=headers)
        print("🔍 Status:", resp.status_code)
        print("🔍 Response:", resp.text)
        resp.raise_for_status()
        return resp.json()


async def get_productos():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{FLASK_API_URL}/productos")
        resp.raise_for_status()
        return resp.json()


async def get_transacciones():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{FLASK_API_URL}/transacciones")
        resp.raise_for_status()
        return resp.json()
