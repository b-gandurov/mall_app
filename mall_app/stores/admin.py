from django.contrib import admin
from .models import Store, Item, Reservation, ItemCategory, StoreCategory


def mark_as_claimed(queryset):
    queryset.update(is_claimed=True)
    mark_as_claimed.short_description = "Mark selected reservations as claimed"


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'working_hours', 'website', 'email', 'phone', 'location')
    search_fields = ('name', 'working_hours', 'website', 'email', 'phone', 'location')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category')
        }),
        ('Contact Information', {
            'fields': ('working_hours', 'website', 'email', 'phone', 'location'),
        }),
    )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'description', 'store', 'available_for_reservation', 'price', 'category', 'quantity', 'reservation_timer')
    search_fields = ('name',)
    list_filter = ('store', 'available_for_reservation',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'reservation_time',)
    search_fields = ('item__name', 'user__email',)
    list_filter = ('reservation_time',)
    actions = [mark_as_claimed]


@admin.register(ItemCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StoreCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
