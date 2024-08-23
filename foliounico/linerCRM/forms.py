from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import RadioSelect

from .enums import Rol
from .models import CustomUser


def validate_integer(value):
    if not value.isdigit():
        raise ValidationError("Please enter a valid integer.")


class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'numero_telefono']


class SignupForm(UserCreationForm):
    codigo_registro = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Codigo'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre / Nombres'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    fecha_de_nacimiento = forms.DateField(required=True, label='Fecha de Nacimiento', widget=forms.DateInput(attrs={'placeholder': 'Fecha Nacimiento', 'type': 'date'}))
    estatura = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(
            attrs={
                'placeholder': 'Estatura Mts.',
                'step': '0.01',  # Permite valores decimales
                'min': '0',  # Valor mínimo, ajusta según necesidad
                'type': 'number',  # Asegura que solo se acepten números
            }
        ))
    peso = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(
            attrs={
                'placeholder': 'Peso Kg.',
                'step': '0.01',  # Permite valores decimales
                'min': '0',  # Valor mínimo, ajusta según necesidad
                'type': 'number',  # Asegura que solo se acepten números
            }
        ))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    numero_telefono = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        validators=[validate_integer]
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirma contraseña'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['numero_telefono', 'last_name', 'first_name', 'fecha_de_nacimiento', 'email']


    def clean_username(self):
        # Skip the username validation
        pass

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden. Vuelva a intentarlo.')

