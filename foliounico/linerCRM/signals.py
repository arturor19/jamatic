# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Pago


@receiver(post_save, sender=Pago)
def generar_recibo_pdf(sender, instance, **kwargs):
    # Solo generar el recibo si no existe
    if not instance.recibo_pdf:
        # Generar el recibo en PDF
        buffer = BytesIO()
        ancho_recibo = 80 * mm
        largo_recibo = 200 * mm
        p = canvas.Canvas(buffer, pagesize=(ancho_recibo, largo_recibo))

        # Agregar la cabecera "JAMATIC"
        p.setFont("Helvetica-Bold", 12)
        p.drawCentredString(ancho_recibo / 2, largo_recibo - 10 * mm, "Recibo pago")
        p.drawCentredString(ancho_recibo / 2, largo_recibo - 20 * mm, "Servicio de Internet")

        # Dibujar una línea debajo de la cabecera
        p.setLineWidth(0.5)
        p.setStrokeColor(colors.black)
        p.line(10 * mm, largo_recibo - 32 * mm, ancho_recibo - 10 * mm, largo_recibo - 32 * mm)

        # Configurar el estilo para el resto del texto
        p.setFont("Helvetica", 10)

        # Añadir el contenido del recibo
        p.drawString(10 * mm, largo_recibo - 40 * mm, f"Recibo: {instance.recibo}")
        p.drawString(10 * mm, largo_recibo - 50 * mm, f"Cliente: {instance.cliente.nombre_completo}")
        p.drawString(10 * mm, largo_recibo - 60 * mm, f"Fecha: {instance.fecha_pago.strftime('%d/%m/%Y')}")
        p.drawString(10 * mm, largo_recibo - 70 * mm, f"Monto: ${instance.monto:.2f}")

        # Dibujar una línea divisoria
        p.line(10 * mm, largo_recibo - 80 * mm, ancho_recibo - 10 * mm, largo_recibo - 80 * mm)

        # Añadir más detalles del recibo si es necesario
        p.drawString(10 * mm, largo_recibo - 90 * mm, "Gracias por su pago.")
        p.drawString(10 * mm, largo_recibo - 100 * mm, "¡Visítenos nuevamente!")

        # Finalizar el PDF
        p.showPage()
        p.save()

        # Guardar el PDF en el campo `recibo_pdf`
        pdf_name = f'recibo_{instance.id}.pdf'
        instance.recibo_pdf.save(pdf_name, ContentFile(buffer.getvalue()))
        buffer.close()
