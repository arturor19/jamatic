from functools import wraps

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionMixin

from .enums import Rol
from .forms import RegistroUsuarioForm
from .models import ReporteFalla, Pago, Cliente, CustomUser, InstalacionDeServicio
from django.db.models import F, ExpressionWrapper, IntegerField, Subquery, OuterRef, Count, Q
from datetime import date

@admin.site.admin_view
def custom_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')  # Ajusta la redirección según tus necesidades

admin.site.logout = custom_logout


class RegistroUsuarioAdmin(BaseUserAdmin):
    form = RegistroUsuarioForm


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Información Usuario'), {'fields': ('fecha_de_alta', 'numero_telefono', 'rol')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',),
        }),
    )
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_staff', "numero_telefono"]
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class AdeudoFilter(SimpleListFilter):
    title = _('adeudo')
    parameter_name = 'adeudo'

    def lookups(self, request, model_admin):
        return (
            ('con_adeudo', _('Con adeudo')),
            ('sin_adeudo', _('Sin adeudo')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'con_adeudo':
            return queryset.filter(
                id__in=[cliente.id for cliente in queryset if cliente.adeudo() > 0]
            )
        if self.value() == 'sin_adeudo':
            return queryset.filter(
                id__in=[cliente.id for cliente in queryset if cliente.adeudo() == 0]
            )

@admin.register(Cliente)
class ClienteAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        'nombre_completo',
        'direccion',
        'telefono',
        'fecha_alta',
        'cuota',
        'meses_atrasados',
        'adeudo',
        'pagar_link',
        'reporte_falla_link',
    )
    search_fields = ('nombre_completo', 'direccion', 'red', 'telefono')
    list_filter = ('fecha_alta', 'nombre_completo', 'telefono', AdeudoFilter)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.rol == Rol.SECRETARIA:
            # Devolver un queryset vacío para que no vea todos los registros
            return qs.none()
        return qs

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.user.rol == Rol.SECRETARIA and search_term:
            # Limitar los resultados de búsqueda solo a los clientes que coinciden con el término de búsqueda
            queryset = Cliente.objects.filter(
                Q(nombre_completo__icontains=search_term) |
                Q(direccion__icontains=search_term) |
                Q(telefono__icontains=search_term)
            )
        return queryset, use_distinct


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin, ExportActionMixin):
    list_display = ('cliente', 'fecha_pago', 'monto', 'recibo')
    search_fields = ('cliente__nombre_completo', 'recibo')
    list_filter = ('fecha_pago',)

    def response_add(self, request, obj, post_url_continue=None):
        # Redirigir al PDF después de agregar un nuevo pago
        return redirect(reverse('mostrar_recibo_pdf', args=[obj.id]))

    def response_change(self, request, obj):
        # Redirigir al PDF después de modificar un pago existente
        return redirect(reverse('mostrar_recibo_pdf', args=[obj.id]))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.rol == Rol.SECRETARIA:
            # Devolver un queryset vacío para que no vea todos los registros
            return qs.none()
        return qs

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.user.rol == Rol.SECRETARIA and search_term:
            # Limitar los resultados de búsqueda solo a los clientes que coinciden con el término de búsqueda
            queryset = Pago.objects.filter(cliente__nombre_completo__icontains=search_term)
        return queryset, use_distinct

@admin.register(InstalacionDeServicio)
class InstalacionDeServicioAdmin(admin.ModelAdmin, ExportActionMixin):
    list_display = ('cliente', 'direccion_cliente', 'fecha_instalacion', 'tecnico', 'servicio_completado')
    search_fields = ('cliente__nombre_completo', 'servicio_completado')
    list_filter = ('fecha_instalacion', 'servicio_completado')


@admin.register(ReporteFalla)
class ReporteFallaAdmin(admin.ModelAdmin, ExportActionMixin):
    list_display = ('cliente', 'descripcion', 'fecha_reporte', 'solucionado')
    search_fields = ('cliente__nombre_completo', 'descripcion')
    list_filter = ('fecha_reporte', 'solucionado')

admin.site.site_header = "Jamatic"
admin.site.site_title = "Portal de administración de Jamatic"
admin.site.index_title = "Bienvenidos al portal de Jamatic"
