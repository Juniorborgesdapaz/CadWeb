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

    
    path('produto/lista', views.produto, name='listaProduto'),
    path('produto/formulario', views.form_produto, name='form_produto'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('remover_produto/<int:id>/', views.remover_produto, name='remover_produto'),
    path('detalhe_produto/<int:id>', views.detalhe_produto, name='detalhe_produto'),
    #ESTOQUE:
    path('ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),
    #TESTE
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),
    path('teste3/', views.teste3, name='teste3'),
    #Ajax
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),
]