from django.shortcuts import render

def home(request):
    return render(request, 'Tempera/home.html')

# Create your views here.
