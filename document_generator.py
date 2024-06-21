from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Generar cupón de pago
def generar_cupon_pago(inquilino, mes, monto, ruta_archivo):
    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    
    # Ajuste de márgenes
    margen_x = 50
    margen_y = 750

    c.drawString(margen_x, margen_y, "Cupon de Pago")
    c.drawString(margen_x, margen_y - 20, f"Inquilino: {inquilino['nombre_completo']}")
    c.drawString(margen_x, margen_y - 40, f"Mes: {mes}")
    c.drawString(margen_x, margen_y - 60, f"Monto: {monto}")
    
    c.showPage()
    c.save()

# Generar certificado de estado
def generar_certificado_estado(inquilino, pagos, ruta_archivo):
    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    
    # Ajuste de márgenes
    margen_x = 50
    margen_y = 750

    c.drawString(margen_x, margen_y, "Certificado de Estado")
    c.drawString(margen_x, margen_y - 20, f"Inquilino: {inquilino['nombre_completo']}")

    y = margen_y - 40
    for pago in pagos:
        c.drawString(margen_x, y, f"Mes: {pago['mes']}, Monto: {pago['monto']}")
        y -= 20

    c.showPage()
    c.save()
