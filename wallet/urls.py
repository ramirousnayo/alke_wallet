from django.urls import path
from . import views

urlpatterns = [
    # Usuario
    path('', views.usuario_list, name='usuario_list'),
    path('usuario/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('crear/', views.usuario_create, name='usuario_create'),
    path('editar/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('eliminar/<int:pk>/', views.usuario_delete, name='usuario_delete'),
    
    # Cuentas
    path('usuario/<int:usuario_id>/nueva-cuenta/', views.cuenta_create, name='cuenta_create'),
    path('cuenta/editar/<int:pk>/', views.cuenta_update, name='cuenta_update'),
    path('cuenta/eliminar/<int:pk>/', views.cuenta_delete, name='cuenta_delete'),

    # Transaccion
    path('transacciones/', views.transaccion_list, name='transaccion_list'),
    path('transacciones/<int:pk>/', views.transaccion_detail, name='transaccion_detail'),
    path('transacciones/nueva/', views.transaccion_create, name='transaccion_create'),
    path('transacciones/editar/<int:pk>/', views.transaccion_update, name='transaccion_update'),
    path('transacciones/eliminar/<int:pk>/', views.transaccion_delete, name='transaccion_delete'),
]
