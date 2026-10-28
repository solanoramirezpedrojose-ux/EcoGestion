from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
    path('detalles/', views.lista_detalles_venta, name='lista_detalles_venta'),
    path('detalles/<int:pk>/', views.detalle_material_venta, name='detalle_material_venta'),
    path('<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('<int:pk>/confirmar/', views.confirmar_venta, name='confirmar_venta'),
    path('<int:pk>/anular/', views.anular_venta, name='anular_venta'),
]