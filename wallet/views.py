from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q, Prefetch
from .models import Usuario, Cuenta, Transaccion
from .forms import UsuarioForm, TransaccionForm, CuentaForm

# ─── USUARIO CRUD ───────────────────────────────────────────────

def usuario_list(request):
    tipo = request.GET.get('tipo', '')
    orden = request.GET.get('orden', '')

    # Caso CON filtro de tipo de cuenta
    if tipo in ['corriente', 'ahorro']:
        # 1. Filtramos los usuarios que tienen al menos una cuenta de ese tipo
        # 2. Anotamos el saldo sumando SOLO las cuentas de ese tipo (ORM filter en Sum)
        # 3. Pre-cargamos SOLO las cuentas de ese tipo (Prefetch)
        usuarios = Usuario.objects.filter(cuentas__tipo_cuenta=tipo).annotate(
            total_saldo=Sum('cuentas__saldo', filter=Q(cuentas__tipo_cuenta=tipo))
        ).prefetch_related(
            Prefetch('cuentas', queryset=Cuenta.objects.filter(tipo_cuenta=tipo))
        ).distinct()
    else:
        # Caso SIN filtro (Todas las Cuentas)
        usuarios = Usuario.objects.annotate(
            total_saldo=Sum('cuentas__saldo')
        ).prefetch_related('cuentas')

    # Ordenamiento por saldo
    if orden == 'saldo_desc':
        usuarios = usuarios.order_by('-total_saldo')
    elif orden == 'saldo_asc':
        usuarios = usuarios.order_by('total_saldo')
    else:
        usuarios = usuarios.order_by('-creado_en')

    return render(request, 'wallet/usuario_list.html', {
        'usuarios': usuarios,
        'tipo': tipo,
        'orden': orden
    })


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


# ─── CUENTA CRUD ────────────────────────────────────────────────

def cuenta_create(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.usuario = usuario
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.get_tipo_cuenta_display()} agregada a {usuario.nombre}.')
            return redirect('usuario_detail', pk=usuario.id)
    else:
        tipo_inicial = request.GET.get('tipo', 'corriente')
        form = CuentaForm(initial={'tipo_cuenta': tipo_inicial})
    
    return render(request, 'wallet/cuenta_form.html', {
        'form': form, 
        'usuario': usuario,
        'titulo': 'Nueva Cuenta'
    })


def cuenta_update(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)
    form = CuentaForm(request.POST or None, instance=cuenta)
    if form.is_valid():
        form.save()
        messages.success(request, f'Cuenta {cuenta.get_tipo_cuenta_display()} actualizada.')
        return redirect('usuario_detail', pk=cuenta.usuario.id)
    return render(request, 'wallet/cuenta_form.html', {
        'form': form, 
        'usuario': cuenta.usuario, 
        'titulo': 'Editar Cuenta'
    })


def cuenta_delete(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)
    usuario_id = cuenta.usuario.id
    if request.method == 'POST':
        tipo = cuenta.get_tipo_cuenta_display()
        cuenta.delete()
        messages.success(request, f'Cuenta {tipo} eliminada.')
        return redirect('usuario_detail', pk=usuario_id)
    return render(request, 'wallet/usuario_confirm_delete.html', {'objeto': cuenta, 'tipo': 'cuenta'})


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
