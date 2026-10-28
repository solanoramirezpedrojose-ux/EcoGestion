from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('<int:pk>/', views.detalle_pago, name='detalle_pago'),
]