from django.urls import path
from . import views
from .views import index, precios_view, taller_view, contacto_view, asistencia

urlpatterns = [
    path('', views.index, name='index'),
    path('precios/', views.precios_view, name='precios'),
    path('taller/', views.taller_view, name='taller'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('asistencia/', views.asistencia, name='asistencia'),
]