from django.core.validators import MaxValueValidator
from django.db import models


from apps.restaurants.models import Restaurant


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.BigIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, related_name="restaurant_name")
