from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Owner(models.Model):

    Owner_name = models.CharField(max_length=20)
    Owner_age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    Owner_phone = models.CharField(max_length=15)
    Owner_email = models.CharField(max_length=30, default='<EMAIL>')
    Owner_address = models.CharField(max_length=100)
    Owner_driver_license=models.CharField(max_length=10, default='none', blank=True)
    def __str__(self) -> str:
        return self.Owner_name

class Vehicle(models.Model):
    Owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    Color = models.CharField(max_length=10)
    Producer = models.CharField(max_length=10)
    Type = models.CharField(max_length=10)
    Year = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2024)])
    speed = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    condition=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])

    def __str__(self) -> str:
        return self.Number

class platenumber(models.Model):
    Owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    plate_number = models.CharField(max_length=10,unique=True)
    def __str__(self) -> str:
        return self.plate_number



class Junction(models.Model):
    Address = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.Address