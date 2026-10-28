from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recolecciones, name='lista_recolecciones'),
    path('detalles/', views.lista_detalles_recoleccion, name='lista_detalles_recoleccion'),
    path('detalles/<int:pk>/', views.detalle_material_recoleccion, name='detalle_material_recoleccion'),
    path('<int:pk>/', views.detalle_recoleccion, name='detalle_recoleccion'),
    path('<int:pk>/confirmar/', views.confirmar_recoleccion,name='confirmar_recoleccion'),
    path('<int:pk>/cancelar/', views.cancelar_recoleccion, name='cancelar_recoleccion'),,
]