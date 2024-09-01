# Create your models here.
import uuid
from datetime import date
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .enums import Rol
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    fecha_de_alta = models.DateField(null=True, blank=True)
    nombre_completo = models.CharField(max_length=255, blank=True)
    rol = models.CharField(max_length=30, choices=Rol.choices, default=Rol.SECRETARIA)
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designa si el usuario puede iniciar sesión en el sitio de administración."),
    )
    numero_telefono = models.CharField(max_length=10, verbose_name="Número de teléfono")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Remove 'username' from REQUIRED_FIELDS

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  # Generate username only if it doesn't exist
            self.username = self.generate_username()
        self.nombre_completo = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def generate_username(self):
        username = f"{self.first_name.lower()}.{self.last_name.lower()}".replace(" ", "")
        count = 1
        while CustomUser.objects.filter(username=username).exists():
            # If the username already exists, append a count to make it unique
            count += 1
            username = f"{self.first_name.lower()}.{self.last_name.lower()}.{count}".replace(" ", "")
        return username

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"


class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion_mac = models.CharField(max_length=17, blank=True, null=True)
    red = models.CharField(max_length=255, blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    cuota = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)  # Agregando el campo cuota

    def __str__(self):
        return self.nombre_completo

    def meses_atrasados(self):
        hoy = timezone.now().date()
        meses_desde_alta = (hoy.year - self.fecha_alta.year) * 12 + hoy.month - self.fecha_alta.month

        # calcular meses pagados con los pagos realizados
        meses_pagados =  sum(pago.monto for pago in self.pagos.all()) / self.cuota

        print(f"meses_pagados: {meses_pagados}")

        return max(0, meses_desde_alta - meses_pagados)

    def adeudo(self):
        # Calcular el total de deuda acumulada en base a los meses atrasados
        total_adeudo = self.meses_atrasados() * self.cuota

        return total_adeudo


    def pagar_link(self):
        url = reverse('admin:linerCRM_pago_add')  # Ajusta 'crm' al nombre de tu aplicación
        return format_html('<a href="{}?cliente={}">Pagar</a>', url, self.id)

    def falla_link(self):
        url = reverse('admin:linerCRM_pago_add')  # Ajusta 'crm' al nombre de tu aplicación
        return format_html('<a href="{}?cliente={}">Pagar</a>', url, self.id)



    def reporte_falla_link(self):
        url = reverse('admin:linerCRM_reportefalla_add')  # Ajusta 'crm' al nombre de tu aplicación
        return format_html('<a href="{}?cliente={}">Reporte de Falla</a>', url, self.id)

    reporte_falla_link.short_description = 'Reporte de Falla'
    pagar_link.short_description = 'Pagar'

class Pago(models.Model):
    cliente = models.ForeignKey('Cliente', related_name='pagos', on_delete=models.CASCADE)
    fecha_pago = models.DateField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    recibo = models.CharField(max_length=255, blank=True, null=True)
    recibo_pdf = models.FileField(upload_to='recibos/', blank=True, null=True)

    def __str__(self):
        return f'{self.cliente.nombre_completo} - {self.fecha_pago}'

    def save(self, *args, **kwargs):
        # Si no hay un número de recibo, generarlo
        if not self.recibo:
            self.recibo = f'Recibo-{self.cliente.id}-{self.fecha_pago}'

        # Llamar al método save del padre para guardar el objeto en la base de datos
        super().save(*args, **kwargs)


class ReporteFalla(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='reportes', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    solucionado = models.BooleanField(default=False)

    def __str__(self):
        return f'Falla de {self.cliente.nombre_completo} - {self.fecha_reporte}'

    class Meta:
        verbose_name_plural = "Reportes de Fallas"


class InstalacionDeServicio(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='instalaciones', on_delete=models.CASCADE)
    fecha_instalacion = models.DateTimeField(auto_now_add=True)
    tecnico = models.ForeignKey(get_user_model(), related_name='instalaciones', on_delete=models.CASCADE)
    servicio_completado = models.BooleanField(default=False)

    def __str__(self):
        return f'Instalación de {self.cliente.nombre_completo} - {self.fecha_instalacion}'

    class Meta:
        verbose_name = "Instalación de Servicio"
        verbose_name_plural = "Instalaciones de Servicio"
