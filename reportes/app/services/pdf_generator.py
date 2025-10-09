from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generar_pdf(datos, titulo="Reporte"):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(titulo)

    pdf.drawString(230, 750, titulo)
    y = 720

    for item in datos:
        pdf.drawString(50, y, str(item))
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer
