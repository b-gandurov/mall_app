from django.contrib import admin

from mall_app.parking.models import CustomerCar, Parking, ParkingRate


class CustomerCarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'customer')
    search_fields = ['license_plate', 'customer__user__email']


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'entrance_date', 'exit_date', 'amount_to_pay')

class ParkingRateAdmin(admin.ModelAdmin):
    list_display = ('free_hours', 'hourly_rate')

admin.site.register(ParkingRate, ParkingRateAdmin)

admin.site.register(CustomerCar, CustomerCarAdmin)
admin.site.register(Parking, ParkingAdmin)
