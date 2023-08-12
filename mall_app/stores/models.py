# mall_app/stores/models.py
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class StoreCategory(Category):
    pass

class ItemCategory(Category):
    pass

class Store(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='stores/', null=True, blank=True)
    category = models.ForeignKey(StoreCategory, related_name='stores', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    available_for_reservation = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(ItemCategory, related_name='items', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    reservation_timer = models.PositiveIntegerField(default=5, help_text="Reservation time in minutes")

    def __str__(self):
        return self.name


class Reservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)
    item_quantity_increased = models.BooleanField(default=False)

    @property
    def is_expired(self):
        expiration_time = self.reservation_time + timedelta(minutes=self.item.reservation_timer)
        return timezone.now() > expiration_time

    def increase_item_quantity_if_expired(self):
        if self.is_expired and not self.is_claimed and not self.item_quantity_increased:
            self.item.quantity += 1
            self.item.save()
            self.item_quantity_increased = True
            self.save()

    def __str__(self):
        return f'{self.user.email} reserved {self.item.name}'
