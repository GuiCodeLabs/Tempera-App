from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario
        fields = [
            'username', 
            'email', 
            'telefone', 
            'data_nascimento', 
            'password1', 
            'password2'
        ]
