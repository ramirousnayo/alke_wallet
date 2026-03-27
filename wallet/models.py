from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    TIPO_CUENTA_CHOICES = [
        ('corriente', 'Cuenta Corriente'),
        ('ahorro', 'Cuenta de Ahorro'),
    ]

    usuario = models.ForeignKey(Usuario, related_name='cuentas', on_delete=models.CASCADE)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, default='corriente')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_tipo_cuenta_display()} - {self.usuario.nombre}"


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
    ]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"
