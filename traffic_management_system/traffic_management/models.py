from django.db import models


class Owner(models.Model):
    Owner_name = models.CharField(max_length=20)
    Owner_phone = models.CharField(max_length=15)
    Owner_email = models.CharField(max_length=30, default='<EMAIL>')
    Owner_address = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.Owner_name

class Vehicle(models.Model):
    Number = models.CharField(max_length=10)
    Owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    Color = models.CharField(max_length=10)
    Producer = models.CharField(max_length=10)
    Type = models.CharField(max_length=10)
    Year = models.IntegerField()
    def __str__(self) -> str:
        return self.Number


class Junction(models.Model):
    Address = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.Address