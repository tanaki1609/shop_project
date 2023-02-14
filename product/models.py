from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
