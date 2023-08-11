from django.db import models
from django.utils import timezone

from mall_app.users.models import UserProfile


class CustomerCar(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "Customer Cars"

    def __str__(self):
        return self.license_plate


class Parking(models.Model):
    MAX_CAPACITY = 400
    non_registered_code = models.CharField(max_length=12, blank=True, null=True)
    license_plate = models.CharField(max_length=20, null=True, blank=True)
    entrance_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    customer_car = models.ForeignKey(CustomerCar, null=True, blank=True, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Parking"

    def __str__(self):
        return self.license_plate if self.license_plate else 'Non-registered car'

    def amount_to_pay(self):
        if self.exit_date or not self.entrance_date:
            return "N/A"

        parking_rate = ParkingRate.objects.first()
        if not parking_rate:
            return "N/A"

        parked_hours = (timezone.now() - self.entrance_date).total_seconds() // 3600
        payable_hours = max(0, parked_hours - parking_rate.free_hours)
        payable_hours_decimal = int(payable_hours)
        amount = payable_hours_decimal * parking_rate.hourly_rate

        return f'{amount:.2f}'

    @classmethod
    def is_capacity_available(cls):
        return cls.objects.filter(exit_date__isnull=True).count() < cls.MAX_CAPACITY


class ParkingRate(models.Model):
    free_hours = models.PositiveIntegerField(default=2)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return f"{self.free_hours} free hours, {self.hourly_rate} per hour"