from django.contrib import admin

from mall_app.parking.models import CustomerCar, Parking, ParkingRate


@admin.register(CustomerCar)
class CustomerCarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'customer')
    search_fields = ['license_plate', 'customer__user__email']


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'entrance_date', 'exit_date', 'amount_to_pay')


@admin.register(ParkingRate)
class ParkingRateAdmin(admin.ModelAdmin):
    list_display = ('free_hours', 'hourly_rate')

