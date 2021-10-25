from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')

def products(request):

    return render(request, 'products.html')

def about(request):

    return render(request, 'about.html')
def contactUs(request):

    return render(request, 'contact.html')