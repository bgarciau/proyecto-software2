from fastapi import FastAPI
from app.routers import reportes

app = FastAPI(title="Microservicio de Reportes")

app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "Microservicio de Reportes funcionando 🚀"}
