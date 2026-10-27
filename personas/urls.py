from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_personas, name = 'lista_personas'),
    path('<int:pk>/', views.detalle_persona, name = 'detalle_persona')
]