from django.contrib import admin

from mall_app.parking.models import CustomerCar, Parking


class CustomerCarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'customer')
    search_fields = ('license_plate',)
    # Other customization options...


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'entrance_date', 'exit_date', 'non_registered_code')
    # Other customization options...


admin.site.register(CustomerCar, CustomerCarAdmin)
admin.site.register(Parking, ParkingAdmin)
