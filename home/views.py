from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from .models import Cliente
from .forms import ClienteForm

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
            messages.warning(request, 'Edição realizda com Sucesso.')
            return render(request, 'categoria/lista.html', {'lista':lista,})

    else: 
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categoria/formulario.html', {'form':form,})


def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.error(request, 'Exclusão realizda com Sucesso.')
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
            messages.warning(request, 'Cliente editado com sucesso.')
            return redirect('lista_cliente')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'cliente/form_cliente.html', {'form': form})

# Função para remover um cliente
def remover_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()
    messages.error(request, 'Cliente removido com sucesso.')
    return redirect('lista_cliente')

# Função para ver os detalhes de um cliente
def detalhe_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhe_cliente.html', {'cliente': cliente})