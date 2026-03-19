from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Usuario, Cuenta, Transaccion
from .forms import UsuarioForm, TransaccionForm

# ─── USUARIO CRUD ───────────────────────────────────────────────

def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'wallet/usuario_list.html', {'usuarios': usuarios})


def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    transacciones = Transaccion.objects.filter(cuenta__usuario=usuario).order_by('-fecha')
    return render(request, 'wallet/usuario_detail.html', {
        'usuario': usuario,
        'transacciones': transacciones,
    })


def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Cuenta.objects.create(usuario=usuario)
            messages.success(request, f'Usuario {usuario.nombre} creado con éxito.')
            return redirect('usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'wallet/usuario_form.html', {'form': form, 'titulo': 'Nuevo Usuario'})


def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, f'Usuario {usuario.nombre} actualizado con éxito.')
        return redirect('usuario_list')
    return render(request, 'wallet/usuario_form.html', {'form': form, 'titulo': 'Editar Usuario'})


def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        nombre = usuario.nombre
        usuario.delete()
        messages.success(request, f'Usuario {nombre} eliminado con éxito.')
        return redirect('usuario_list')
    return render(request, 'wallet/usuario_confirm_delete.html', {'objeto': usuario, 'tipo': 'usuario'})


# ─── TRANSACCION CRUD ────────────────────────────────────────────

def transaccion_list(request):
    transacciones = Transaccion.objects.select_related('cuenta__usuario').order_by('-fecha')
    return render(request, 'wallet/transaccion_list.html', {'transacciones': transacciones})


def transaccion_detail(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    return render(request, 'wallet/transaccion_detail.html', {'transaccion': transaccion})


def _actualizar_saldo(cuenta):
    """Recalcula y guarda el saldo real de la cuenta según sus transacciones."""
    from django.db.models import Sum
    depositos = cuenta.transaccion_set.filter(tipo='deposito').aggregate(total=Sum('monto'))['total'] or 0
    retiros   = cuenta.transaccion_set.filter(tipo='retiro').aggregate(total=Sum('monto'))['total'] or 0
    cuenta.saldo = depositos - retiros
    cuenta.save()


def transaccion_create(request):
    form = TransaccionForm(request.POST or None)
    if form.is_valid():
        transaccion = form.save()
        _actualizar_saldo(transaccion.cuenta)
        messages.success(request, 'Transacción registrada con éxito.')
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_form.html', {'form': form, 'titulo': 'Nueva Transacción'})


def transaccion_update(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    cuenta_anterior = transaccion.cuenta
    form = TransaccionForm(request.POST or None, instance=transaccion)
    if form.is_valid():
        transaccion_guardada = form.save()
        _actualizar_saldo(cuenta_anterior)
        if transaccion_guardada.cuenta != cuenta_anterior:
            _actualizar_saldo(transaccion_guardada.cuenta)
        messages.success(request, 'Transacción actualizada con éxito.')
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_form.html', {'form': form, 'titulo': 'Editar Transacción'})


def transaccion_delete(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        cuenta = transaccion.cuenta
        transaccion.delete()
        _actualizar_saldo(cuenta)
        messages.success(request, 'Transacción eliminada con éxito.')
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_confirm_delete.html', {'objeto': transaccion, 'tipo': 'transacción'})
