from django.forms import ModelForm
from django import forms
from .models import *

class CategoriaForm(forms.ModelForm):
     class Meta:
          model = Categoria
          fields = ['nome', 'ordem',]
          exclude = ['senha',]   
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
          return nome
     
     def clean_ordem(self):
          ordem = self.cleaned_data.get('ordem')
          if ordem <= 0:
               raise forms.ValidationError("O campo ordem tem que ser superior a 0.")
          return ordem

