from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # path('', home, name='home'),
    path('', products, name='home'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('products/', products, name='products'),
    path('new-products/', newest_products, name='newest_products'),
    path('low-price-products/', low_price_products, name='low_price_products'),
    path('high-price-products/', high_price_products, name='high_price_products'),
    path('product/<slug:slug>/', product, name='product'),
    path('about/', about, name='about'),
    path('contact/', contact_us, name='contact'),
    path('cart/', cart, name='cart'),
    path('customer-account/', account, name='customer_account'),

    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-wishlist/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', remove_from_wishlist, name='remove_from_wishlist'),
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
