# from django.contrib import admin
# from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib import admin
from django.urls import path
#from django_otp.admin import OTPAdminSite

# from django_otp.admin import OTPAdminSite

from .views import HomePageView, mostrar_recibo_pdf
from .views import signup

#admin.site.__class__ = OTPAdminSite


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='index'),
    path('signup/', signup, name='signup'),
    path('recibo/<int:pago_id>/', mostrar_recibo_pdf, name='mostrar_recibo_pdf'),
 #   path('es-mx/admin/logout/', admin_site.logout, name='admin_logout'),  # Ruta personalizada para cerrar sesión
 #   path('es-mx/admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
