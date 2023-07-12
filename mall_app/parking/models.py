from django.db import models

from mall_app.users.models import UserProfile


class CustomerCar(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=20, unique=True)
    car_type = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Customer Cars"

    def __str__(self):
        return self.license_plate


class Parking(models.Model):
    MAX_CAPACITY = 400
    license_plate = models.ForeignKey(CustomerCar, null=True, blank=True, on_delete=models.CASCADE)
    entrance_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Parking"

    def __str__(self):
        return self.license_plate.license_plate if self.license_plate else 'Non-registered car'

    @classmethod
    def is_capacity_available(cls):
        return cls.objects.filter(exit_date__isnull=True).count() < cls.MAX_CAPACITY

