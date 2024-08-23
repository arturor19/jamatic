import datetime
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .enums import Rol


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define la hora de inicio y fin de la restricción
        unrestriction_start = datetime.time(5, 00)
        unrestriction_end = datetime.time(18, 30)

        # Obtén la hora actual
        current_time = datetime.datetime.now().time()

        print(unrestriction_start, current_time, unrestriction_end)

        # Verifica si la hora actual está dentro del rango restringido
        if not unrestriction_start <= current_time <= unrestriction_end:
            # Verifica si el usuario está autenticado y tiene el rol restringido
            if request.user.is_authenticated and request.user.rol != Rol.SUPERADMIN:
                return HttpResponseForbidden("Acceso restringido durante estas horas.")
