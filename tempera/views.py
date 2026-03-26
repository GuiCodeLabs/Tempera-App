from django.shortcuts import render

def home(request):
    return render(request, 'tempera/home.html')

# Create your views here.
