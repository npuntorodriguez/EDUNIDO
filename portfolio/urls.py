from django.urls import path
from . import views
from .views import index, precios_view, taller_view, contacto_view, asistencia, login_usuario, logout_usuario

urlpatterns = [
    path('', views.index, name='index'),
    path('precios/', views.precios_view, name='precios'),
    path('taller/', views.taller_view, name='taller'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('asistencia/', views.asistencia, name='asistencia'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    # Programas
    path('programas/', views.programa_list, name='programa_list'),
    path('programas/crear/', views.programa_create, name='programa_create'),
    path('programas/editar/<int:pk>/', views.programa_edit, name='programa_edit'),
    path('programas/eliminar/<int:pk>/', views.programa_delete, name='programa_delete'),

    # Asignaturas
    path('asignaturas/', views.asignatura_list, name='asignatura_list'),
    path('asignaturas/crear/', views.asignatura_create, name='asignatura_create'),
    path('asignaturas/editar/<int:pk>/', views.asignatura_edit, name='asignatura_edit'),
    path('asignaturas/eliminar/<int:pk>/', views.asignatura_delete, name='asignatura_delete'),
]