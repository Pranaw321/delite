from django.db import models

from django.db import models

# from django.contrib.auth.models import User
from apps.restaurants.models import Restaurant


class Category(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'))
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    img = models.ImageField(null=True)


class Item(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'))

    TYPE_CHOICES = (('veg', 'Veg'),
                    ('nonveg', 'Nonveg'),
                    ('vegan', 'Vegan'))
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True)
    img = models.ImageField(null=True)
    recipe = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='veg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='item_category')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quantity(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=False)  # it will add on price on base price
    # offerPrice = models.IntegerField(null=False)
    desc = models.CharField(max_length=255, null=True),
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)


class AddsOn(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=False)  # it will add on price on base price
    desc = models.CharField(max_length=255, null=True),
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
