from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/lista', views.categoria, name="lista"),
    path('categoria/formulario', views.form_categoria, name='form_categoria'),
    path('detalhe_categoria/<int:id>', views.detalhe_categoria, name='detalhe_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('remover_categoria/<int:id>/', views.remover_categoria, name='remover_categoria'),

    path('cadastrar/', views.form_cliente, name='cadastrar_cliente'),
    path('lista/', views.lista_cliente, name='lista_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('remover/<int:id>/', views.remover_cliente, name='remover_cliente'),
    path('detalhe/<int:id>/', views.detalhe_cliente, name='detalhe_cliente'),
    
]