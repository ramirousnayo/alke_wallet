from django.shortcuts import render, get_object_or_404, redirect
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
            return redirect('usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'wallet/usuario_form.html', {'form': form, 'titulo': 'Nuevo Usuario'})


def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('usuario_list')
    return render(request, 'wallet/usuario_form.html', {'form': form, 'titulo': 'Editar Usuario'})


def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'wallet/usuario_confirm_delete.html', {'objeto': usuario, 'tipo': 'usuario'})


# ─── TRANSACCION CRUD ────────────────────────────────────────────

def transaccion_list(request):
    transacciones = Transaccion.objects.select_related('cuenta__usuario').order_by('-fecha')
    return render(request, 'wallet/transaccion_list.html', {'transacciones': transacciones})


def transaccion_detail(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    return render(request, 'wallet/transaccion_detail.html', {'transaccion': transaccion})


def transaccion_create(request):
    form = TransaccionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_form.html', {'form': form, 'titulo': 'Nueva Transacción'})


def transaccion_update(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    form = TransaccionForm(request.POST or None, instance=transaccion)
    if form.is_valid():
        form.save()
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_form.html', {'form': form, 'titulo': 'Editar Transacción'})


def transaccion_delete(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('transaccion_list')
    return render(request, 'wallet/transaccion_confirm_delete.html', {'objeto': transaccion, 'tipo': 'transacción'})
