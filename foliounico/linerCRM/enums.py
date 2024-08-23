from django.db import models
from django.utils.translation import gettext_lazy as _


class Rol(models.TextChoices):
    SECRETARIA = "Secretaria", _("Secretaria")
    SUPERADMIN = "Superadmin", _("Superadmin")

