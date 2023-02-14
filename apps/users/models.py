from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.restaurants.models import Restaurant


class Admin(models.Model):
    class AdminType(models.TextChoices):
        SUPER_ADMIN = 'SA', _('SuperAdmin')
        ADMIN = 'AD', _('Admin')

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.BigIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    type = models.CharField(
        max_length=2,
        choices=AdminType.choices,
        default=AdminType.ADMIN,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, related_name="restaurant_name")


class User(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.BigIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
