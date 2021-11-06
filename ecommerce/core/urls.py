from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # path('', home, name='home'),
    path('', products, name='home'),
    path('products/', products, name='products'),
    path('product/<slug:slug>/', product, name='product'),
    path('about/', about, name='about'),
    path('contact/', contactUs, name='contact'),
    path('cart/', cart, name='cart'),

    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    # path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-from-cart/<slug:slug>/', reduce_from_cart, name='reduce-from-cart'),
    # path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
        #  name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', payment, name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('checkout/', checkout, name='checkout'),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('create-payment-intent/', create_checkout_session, name='create-checkout'),
]
