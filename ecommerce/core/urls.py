from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('about/', about, name='about'),
    path('contact/', contactUs, name='contact'),
]
