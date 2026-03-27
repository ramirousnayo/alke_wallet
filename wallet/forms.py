from django import forms
from .models import Usuario, Transaccion, Cuenta

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email']


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['tipo_cuenta', 'saldo', 'activa']
        labels = {
            'tipo_cuenta': 'Tipo de Cuenta',
            'saldo': 'Saldo Inicial',
            'activa': '¿Activa?',
        }


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
