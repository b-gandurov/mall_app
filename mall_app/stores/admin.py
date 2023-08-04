# mall_app/stores/admin.py

from django.contrib import admin
from .models import Store, Item, Reservation, Category


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'store', 'available_for_reservation', 'price', 'category', 'quantity')
    search_fields = ('name',)
    list_filter = ('store', 'available_for_reservation',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'reservation_time',)
    search_fields = ('item__name', 'user__email',)
    list_filter = ('reservation_time',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
