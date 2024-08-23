# Create your views here.

# Create your views here.

from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Pago


class HomePageView(TemplateView):
    template_name = 'home.html'


from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Replace 'home' with the URL name of your desired success page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def mostrar_recibo_pdf(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)

    # Abrir el PDF que ya está guardado en el campo recibo_pdf
    if pago.recibo_pdf:
        with open(pago.recibo_pdf.path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="recibo_{pago.id}.pdf"'
            return response
    else:
        return HttpResponse("No se ha generado un recibo PDF para este pago.")
