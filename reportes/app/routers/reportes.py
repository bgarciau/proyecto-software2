from fastapi import APIRouter, Response
from app.services.pdf_generator import generar_pdf
from app.services.excel_generator import generar_excel
from app.utils.api_client import get_usuarios, get_productos, get_transacciones
from fastapi import Depends, Request
from fpdf import FPDF

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# --- Reporte de usuarios (PDF) ---
@router.get("/usuarios/pdf")
async def reporte_usuarios_pdf(request: Request):
    token = request.headers.get("Authorization")
    print("token:", token)
    if not token or not token.startswith("Bearer "):
        return Response("Token no proporcionado", status_code=401)
    token = token.split(" ")[1]
    usuarios = await get_usuarios(token = token)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Usuarios", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(40, 10, "ID")
    pdf.cell(60, 10, "Nombre")
    pdf.cell(60, 10, "Email")
    pdf.ln(10)
    for user in usuarios:
        pdf.cell(40, 10, str(user["id"]))
        pdf.cell(60, 10, user["name"])
        pdf.cell(60, 10, user["email"])
        pdf.ln(10)
    from io import BytesIO
    stream = BytesIO(pdf.output(dest='S').encode('latin-1'))
    return Response(stream.read(), media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=usuarios.pdf"})

# Reporte de usuarios (Excel)
@router.get("/usuarios/excel")
async def reporte_usuarios_excel(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return Response("Token no proporcionado", status_code=401)
    token = token.split(" ")[1]
    usuarios = await get_usuarios(token=token)
    buffer = generar_excel(usuarios, "Usuarios")
    return Response(
        buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_usuarios.xlsx"}
    )

#reporte de productos (PDF)
@router.get("/productos/pdf")
async def reporte_productos_pdf():
    productos = await get_productos()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Productos", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(40, 10, "ID")
    pdf.cell(60, 10, "Nombre")
    pdf.cell(60, 10, "Descripción")
    pdf.cell(30, 10, "Precio")
    pdf.cell(20, 10, "Stock")
    pdf.ln(10)
    for producto in productos:
        pdf.cell(40, 10, str(producto["_id"]))
        pdf.cell(60, 10, producto["nombre"])
        pdf.cell(60, 10, producto["descripcion"])
        pdf.cell(30, 10, str(producto["precio"]))
        pdf.cell(20, 10, str(producto["stock"]))
        pdf.ln(10)
    from io import BytesIO
    stream = BytesIO(pdf.output(dest='S').encode('latin-1'))
    return Response(stream.read(), media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=productos.pdf"})

# --- Reporte de productos (Excel) ---
@router.get("/productos/excel")
async def reporte_productos_excel():
    productos = await get_productos()
    buffer = generar_excel(productos, "Productos")
    return Response(
        buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_productos.xlsx"}
    )

# --- Reporte de transacciones (PDF) ---
@router.get("/transacciones/pdf")
async def reporte_transacciones_pdf():
    transacciones = await get_transacciones()
    buffer = generar_pdf(transacciones, "Reporte de Transacciones")
    # return Response(
    #     buffer.getvalue(),
    #     media_type="application/pdf",
    #     headers={"Content-Disposition": "attachment; filename=reporte_transacciones.pdf"}
    # )
    pdf = FPDF()
    pdf.add_page() 
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Transacciones", ln=True, align='C')
    pdf.ln(10)  
    pdf.cell(70, 10, "ID")
    pdf.cell(20, 10, "Tipo")   
    pdf.cell(20, 10, "Usuario ID")
    pdf.cell(50, 10, "Producto ID")
    pdf.cell(30, 10, "Cantidad")
    pdf.cell(40, 10, "Monto Total")
    pdf.cell(40, 10, "Fecha")
    pdf.ln(10)
    for transaccion in transacciones:
        pdf.cell(70, 10, str(transaccion["_id"]))
        pdf.cell(20, 10, transaccion["tipo"])
        pdf.cell(20, 10, str(transaccion["usuario_id"]))
        pdf.cell(50, 10, str(transaccion["producto_id"]))
        pdf.cell(30, 10, str(transaccion["cantidad"]))
        pdf.cell(40, 10, str(transaccion["monto_total"]))
        pdf.cell(40, 10, transaccion["fecha"])
        pdf.ln(10)
    from io import BytesIO
    stream = BytesIO(pdf.output(dest='S').encode('latin-1'))
    return Response(stream.read(), media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=transacciones.pdf"})

# --- Reporte de transacciones (Excel) ---
@router.get("/transacciones/excel")
async def reporte_transacciones_excel():
    transacciones = await get_transacciones()
    buffer = generar_excel(transacciones, "Transacciones")
    return Response(
        buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_transacciones.xlsx"}
    )