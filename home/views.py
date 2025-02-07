from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from .models import Cliente
from .forms import ClienteForm
from .models import Produto, Estoque
from .forms import ProdutoForm, EstoqueForm
from django.http import JsonResponse
from django.apps import apps
def index(request):
    return render(request,'index.html')

def categoria(request): 
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if (request.method == 'POST'):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            salvando = form.save()
            lista=[]
            lista.append(salvando)
            messages.success(request, 'Operação realizda com Sucesso.')
            return render(request, 'categoria/lista.html', {'lista':lista,})
        
    else: 
        form = CategoriaForm()
    
    return render(request, 'categoria/formulario.html', {'form': form,})


def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except:
        messages.error(request, 'Não encotramos seus registros')
        return redirect('lista')

    if (request.method == 'POST'):
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            lista=[]
            lista.append(categoria)
            messages.success(request, 'Edição realizda com Sucesso.')
            return render(request, 'categoria/lista.html', {'lista':lista,})

    else: 
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categoria/formulario.html', {'form':form,})


def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Exclusão realizda com Sucesso.')
    except:
        messages.error(request, 'Não encotramos seus registros')
        return redirect('lista')
    
    return redirect('lista')
    # return render(request, 'categoria/lista.html')


def detalhe_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
    except:
        messages.error(request, 'Não encotramos seus registros')
        return redirect('lista')

    return render(request, 'categoria/detalhes.html', {'categoria':categoria,})

def lista_cliente(request):
    clientes = Cliente.objects.all().order_by('-id')
    return render(request, 'cliente/lista_cliente.html', {'lista': clientes})

# Função para cadastrar um novo cliente
def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('lista_cliente')  # Redireciona para a lista de clientes
    else:
        form = ClienteForm()
    
    return render(request, 'cliente/form_cliente.html', {'form': form})

# Função para editar um cliente
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente editado com sucesso.')
            return redirect('lista_cliente')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'cliente/form_cliente.html', {'form': form})

# Função para remover um cliente
def remover_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()
    messages.success(request, 'Cliente removido com sucesso.')
    return redirect('lista_cliente')

# Função para ver os detalhes de um cliente
def detalhe_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhe_cliente.html', {'cliente': cliente})


# Função para produto
def produto(request):
    contexto = {
        'listaProduto': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

# Cadastro de produto
def form_produto(request):
    if (request.method == 'POST'):
        form = ProdutoForm(request.POST)
        if form.is_valid():
            salvando = form.save()
            listaProduto=[]
            listaProduto.append(salvando)
            messages.success(request, 'Operação realizda com Sucesso.')
            return render(request, 'produto/lista.html', {'listaProduto':listaProduto,})
        
    else: 
        form = ProdutoForm()
    
    return render(request, 'produto/formulario.html', {'form': form,})

# Edição de produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)  # Adicionado request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto editado com sucesso.')
            return redirect('listaProduto')
        else:
            messages.error(request, 'Erro ao editar produto. Verifique os dados.')
    else: 
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})

# Remoção de produto
def remover_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto.delete()
    messages.success(request, 'Produto removido com sucesso.')
    return redirect('listaProduto')

# Detalhes de produto
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})

# Ajuste de estoque
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    estoque = produto.estoque if hasattr(produto, 'estoque') else None  # Verifica se o produto tem estoque
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.produto = produto
            estoque.save()
            messages.success(request, 'Estoque ajustado com sucesso.')
            return redirect('listaProduto')
        else:
            messages.error(request, 'Erro ao ajustar estoque. Verifique os dados.')
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})

def teste1(request):
    return render (request, 'testes/teste1.html')

def teste2(request):
    return render (request, 'testes/teste2.html')

def teste3(request):
    return render (request, 'testes/teste3.html')

def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)



def pedido(request):
    listaPedido = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'listaPedido': listaPedido})


def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  # Redireciona para a listagem
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)# cria um formulario com o novo pedido
        return render(request, 'pedido/formulario.html',{'form': form,})
    else: # se for metodo post, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('listaPedido')




# def detalhes_pedido(request, id):
#     try:
#         pedido = Pedido.objects.get(pk=id)
#     except Pedido.DoesNotExist:
#         messages.error(request, 'Registro não encontrado')
#         return redirect('listaPedido')   
    
#     if request.method == 'GET':
#         itemPedido = ItemPedido(pedido=pedido)
#         form = ItemPedidoForm(instance=itemPedido)
#     else: # method Post
#         form = ItemPedidoForm(request.POST)
#         if form.is_valid():
#             item_pedido = form.save(commit=False) # commit=False retorna o objeto item_pedido vindo do form para fazermos modificações adicionais antes de salvá-la, colocar o preço do produto, verificar estoque.
#             item_pedido.preco = item_pedido.produto.preco # acessando o produto do relacionamento
#             try:
#                 if item_pedido.produto.estoque >= item_pedido.qtde:
#                         item_pedido.produto.estoque = item_pedido.produto.estoque -  item_pedido.qtde
#                         item_pedido.save()
#                 return item_pedido.produto.estoque
#             except:
#                 messages.error(request, 'Quantidade pedida é insuficientes para o que tem no estoque.')
#                 # exibe uma mensagem informando sobre isso não ter em estoque
#             # realizar aqui o tratamento do estoque, para isso
#             # Pegar o estoque (item_pedido.produto.estoque do relacionamento) atual 
#             # verificar se a quantidade (item_pedido.produto.estoque.qtde) é suficiente para o item solicitado (item_pedido.qtde)
#             # Se não houver estoque suficiente, você pode adicionar uma mensagem de erro e não salvar a operação
#             # Se sim, decrementar a quantidade do item no estoque do produto e salvar os objetos estoque e item_pedido
#         else:
#              messages.error(request, 'Erro ao adicionar produto')
                  
#     contexto = {
#         'pedido': pedido,
#         'form': form,
#     }
#     return render(request, 'pedido/detalhes.html',contexto )

def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:  # method Post
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # commit=False permite modificações antes de salvar
            item_pedido.preco = item_pedido.produto.preco  # Acessando o preço do produto relacionado
            estoque_atual = item_pedido.produto.estoque
            
            # Verificação do estoque
            print (f'Quantidade pedido: {item_pedido.qtde}')
            print (f'Estoque: {estoque_atual.qtde}')
            if item_pedido.qtde > estoque_atual.qtde:
                messages.error(request, 'Estoque insuficiente para este produto')
            else:
                # Decrementando a quantidade do estoque
                estoque_atual.qtde = estoque_atual.qtde - item_pedido.qtde
                item_pedido.produto.estoque.qtde = estoque_atual
                item_pedido.produto.estoque.save()   # Salvando a atualização do estoque
                item_pedido.save()  # Salvando o item do pedido
                print (f'atualizado: {estoque_atual.qtde}')

                messages.success(request, 'Produto adicionado com sucesso!')
                itemPedido = ItemPedido(pedido=pedido)
                form = ItemPedidoForm(instance=itemPedido)
        else:
            messages.error(request, 'Erro ao adicionar produto')


    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)


def editar_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except:
        messages.error(request, 'Registro não encontrado')
        return redirect('listaPedido')

    if (request.method == 'POST'):
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            produto = form.save()
            listaPedido=[]
            listaPedido.append(produto)
            # return render(request, 'produto/lista.html', {'listaProduto':listaProduto,})
            return redirect('listaPedido')

    else: 
        form = PedidoForm(instance=pedido)
    
    return render(request, 'pedido/formulario.html', {'form':form,})

def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)



    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)

def remover_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
        pedido.delete()
        messages.success(request, 'Exclusão realizda com Sucesso.')
    except:
        messages.error(request, 'Registro não encontrado')
        return redirect('listaPedido')
    
    return redirect('listaPedido')


def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
         
    pedido = item_pedido.pedido  # Acessa o pedido diretamente do item
    quantidade_anterior = item_pedido.qtde  # Armazena a quantidade anterior
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # prepara a instância do item_pedido sem persistir ainda
            print(item_pedido.produto.id)

            nova_quantidade_item = item_pedido.qtde
            estoque_atual = item_pedido.produto.estoque.qtde

            if estoque_atual >= nova_quantidade_item:
                estoque_atual = estoque_atual + quantidade_anterior  
                estoque_atual = estoque_atual - nova_quantidade_item
                
                item_pedido.produto.estoque.qtde = estoque_atual

                item_pedido.produto.estoque.save()
                item_pedido.save()
                messages.success(request, 'Operação realizada com Sucesso')

            else:
                messages.success(request, 'Quantidade em estoque insuficiente para o produto.')

            # realizar aqui o tratamento do estoque
            # Pegar a nova quantidade do item pedido
            # Obtém o estoque atual do produto
            # Verifica se há estoque suficiente para a nova quantidade
            # Se não mostras msg Quantidade em estoque insuficiente para o produto.
            # Se sim
            # Pegar a quantidade anterior ao estoque
            # Decrementa a nova quantidade do estoque
            # Salva as alterações no estoque
            # Salva o item do pedido após ajustar o estoque

            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = ItemPedidoForm(instance=item_pedido)
        
    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)


def form_pagamento(request,id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Operação realizada com Sucesso')
            pagamento = Pagamento(pedido=pedido)
            form = PagamentoForm(instance=pagamento)
    else: 
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)
        
        
    # prepara o formulário para um novo pagamento

    contexto = {
        'pedido': pedido,
        'form': form,
    }    
    return render(request, 'pedido/pagamento.html',contexto)