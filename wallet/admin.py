from django.contrib import admin
from .models import Usuario, Cuenta, Transaccion

admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(Transaccion)
