from openpyxl import Workbook
from io import BytesIO

def generar_excel(datos, nombre_hoja="Reporte"):
    wb = Workbook()
    ws = wb.active
    ws.title = nombre_hoja

    if not datos:
        ws.append(["Sin datos"])
    else:
        # Encabezados
        ws.append(list(datos[0].keys()))
        # Filas
        for fila in datos:
            ws.append(list(fila.values()))

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
