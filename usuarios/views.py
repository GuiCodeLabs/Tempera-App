from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UsuarioCadastroForm

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = UsuarioCadastroForm()
        
    return render(request, 'criar_usuario.html', {'form': form})
# Create your views here.
