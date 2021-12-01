from django.contrib import admin
from .models import *


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item')
    list_filter = ('user', 'item')

@admin.register(ManageOrder)
class ManageOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status','payment')
    list_filter = ('order', 'status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'price',
        'discount_price',
        'category',
    )
    search_fields = ( 'title','slug',)
    list_display_links = ('id', 'title',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered', 'item', 'quantity')
    list_filter = ('user', 'ordered', 'item')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'start_date',
        'ordered_date',
        'ordered',
        'payment',
    )
    list_filter = (
        'user',
        'start_date',
        'ordered_date',
        'ordered',
        'payment',
    )
    raw_id_fields = ('items',)
    list_display_links = ('id', 'user',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'shipping_address',
        'zip',
        'default',
    )
    list_filter = ('user', 'default')
    list_display_links = ('id', 'shipping_address',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_charge_id', 'user', 'amount', 'timestamp')
    list_filter = ('user', 'timestamp')
    list_display_links = ('id', 'stripe_charge_id',)










