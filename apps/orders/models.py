from django.db import models

from django.db import models


# from django.contrib.auth.models import User
from apps.menus.models import Item
from apps.restaurants.models import Restaurant
from apps.users.models import User


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'))
    PAYMENT_STATUS = (
        ('completed', 'Completed'),
        ('at_counter', 'At_Counter'),
        ('pending', 'pending'))
    amount = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    payment = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='at_counter')
    order_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
