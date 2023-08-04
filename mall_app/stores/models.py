# mall_app/stores/models.py

from django.db import models
from django.conf import settings


class Store(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='stores/', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    available_for_reservation = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} reserved {self.item.name}'
