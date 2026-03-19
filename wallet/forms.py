from django import forms
from .models import Usuario, Transaccion

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email']


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'descripcion']
        labels = {
            'cuenta': 'Cuenta',
            'tipo': 'Tipo de operación',
            'monto': 'Monto',
            'descripcion': 'Descripción (opcional)',
        }
