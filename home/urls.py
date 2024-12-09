from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/lista', views.categoria, name="lista"),
    path('categoria/formulario', views.form_categoria, name='form_categoria'),
    path('categoria/detalhe_categoria/<int:pk>', views.detalhe_categoria, name='detalhe_categoria'),
    path('editar_categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('delete_categotia/<int:pk>/', views.delete_categotia, name='delete_categotia'),
]