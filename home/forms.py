from django.forms import ModelForm
from django import forms
from .models import *

from datetime import date

class CategoriaForm(forms.ModelForm):
     class Meta:
          model = Categoria
          fields = ['nome', 'ordem',]
          # exclude = ['senha',]  #Exclui campos especificos 
          widgets = {
               'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome', 'style': 'margin-bottom::15px'}),
               'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': 'Ordem'}),
          }
          labels = {
               'nonme': 'Informe o nome do produto: ',
               'ordem': 'Informe o número da ordem: ',
          }

     def clean_nome(self):
          nome = self.cleaned_data.get('nome')
          if len(nome) < 3:
               raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
          
          # if Categoria.objects.filter(nome=nome).exists():
          #      raise forms.ValidationError("Já existe uma categoria com esse mesmo nome.")
          
          return nome
     
     def clean_ordem(self):
          ordem = self.cleaned_data.get('ordem')
          if ordem <= 0:
               raise forms.ValidationError("O campo ordem tem que ser superior a 0.")
          
          # if Categoria.objects.filter(ordem=ordem).exists():
          #      raise forms.ValidationError("O númera da ordem digitada já esta sendo utilizada.")
          
          return ordem


class ClienteForm(forms.ModelForm):
     class Meta:
          model = Cliente 
          fields = ['nome', 'cpf', 'datanasc',]
          widgets = {
               'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
               'cpf':forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
               'datanasc':forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
          }

     def clean_nome(self):
         nome = self.cleaned_data.get('nome')
         if Cliente.objects.filter(nome=nome).exclude(pk=self.instance.pk).exists():
             raise forms.ValidationError("Já existe um cliente com esse nome.")
         if len(nome) < 3:
             raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
         return nome

     def clean_cpf(self):
         cpf = self.cleaned_data.get('cpf')
         if Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
             raise forms.ValidationError("Já existe um cliente com esse C.P.F.")
         if len(cpf) != 14:  # Exemplo: "000.000.000-00"
             raise forms.ValidationError("O CPF deve conter 14 caracteres (incluindo pontos e traços).")
         return cpf

     
     def clean_datanasc(self):
          datanasc = self.cleaned_data.get('datanasc')
          if not datanasc:
               raise forms.ValidationError("A data de nascimento é obrigatória.")
          if datanasc >= date.today():
               raise forms.ValidationError("A data de nascimento não pode ser maior ou igual à data atual.")
          if datanasc.year < 1900:
               raise forms.ValidationError("A data de nascimento não pode ser anterior ao ano de 1900.")
          return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria','img_base64']
        widgets = {
            #'categoria': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.HiddenInput() ,
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(), 
            # a classe money mascara a entreda de valores monetários, está em base.html
            #  jQuery Mask Plugin
            'preco':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }


    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True   


class EstoqueForm(forms.ModelForm):
     class Meta:
          model = Estoque
          fields = ['produto', 'qtde']

          widgets = {
               'produto': forms.HiddenInput(),
               'qtde': forms.TextInput(attrs={'class': 'inteiro form-control',}),
          }  

class PedidoForm(forms.ModelForm):
     class Meta:
          model = Pedido
          fields = ['cliente']
          widgets = {
               'cliente': forms.HiddenInput(),
          }



class ItemPedidoForm(forms.ModelForm):
     class Meta:
          model = ItemPedido
          fields = ['pedido', 'produto', 'qtde']

          widgets = {
               'pedido': forms.HiddenInput(),
               'produto': forms.HiddenInput(),
               'qtde': forms.TextInput(attrs={'class': 'inteiro form-control',}),
          }
     
     def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if not isinstance(qtde, int) or qtde < 0:
            raise ValidationError('A quantidade deve ser um número inteiro positivo.')
        return qtde

class PagamentoForm(forms.ModelForm):
     class Meta:
          model = Pagamento
          fields = ['pedido', 'forma', 'valor']
          widgets = {
               'pedido': forms.HiddenInput(),
               'forma': forms.Select(attrs={'class': 'form-control'}),
               'valor': forms.TextInput(attrs={
                    'class': 'money form-control',
                    'maxlenght': '500',
                    'placeholder': '0.000,00',
            }),
         }
     
     def __init__(self, *args, **kwargs):
          super(PagamentoForm, self).__init__(*args, **kwargs)
          self.fields['valor'].localize = True 
          self.fields['valor'].widget.is_localized = True 

     
     def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        pedido = self.cleaned_data.get('pedido')

        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")

        if pedido:
            debito = pedido.debito  # Obtém o valor do débito do pedido
            if valor > debito:
                raise forms.ValidationError("O valor do pagamento não pode ser maior que o débito do pedido.")

        return valor