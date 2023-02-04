from django.db import models


from django.db import models


# from django.contrib.auth.models import User


class Restaurant(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'))
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.IntegerField(null=True),
    address1 = models.CharField("Address line 1", max_length=1024, ),
    address2 = models.CharField("Address line 2", max_length=1024, )
    zip_code = models.CharField("ZIP / Postal code", max_length=12),
    city = models.CharField("City", max_length=1024)
    country = models.CharField(max_length=1024)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
