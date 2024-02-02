from django.db import models


class Owner(models.Model):
    Owner_name = models.CharField(max_length=20)
    Owner_age = models.IntegerField()
    Owner_phone = models.CharField(max_length=15)
    Owner_email = models.CharField(max_length=30, default='<EMAIL>')
    Owner_address = models.CharField(max_length=100)
    Owner_driver_license = models.CharField(max_length=10, default='0000000000', blank=False, unique=True)


class Plates(models.Model):
    Number = models.CharField(max_length=10, unique=True)
    Status = models.CharField(max_length=10, default='available')

    def __str__(self):
        return self.Number

class Vehicle(models.Model):
    Owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    Color = models.CharField(max_length=20)
    VType = models.CharField(max_length=50)
    Speed = models.IntegerField(default=0)
    Condition = models.IntegerField(default=100)
    PlateNumber = models.ForeignKey(Plates, null=True, on_delete=models.SET_NULL)


class Junction(models.Model):
    Address = models.CharField(max_length=100)
    Light = models.IntegerField(default=1)


class Log(models.Model):
    Junction = models.CharField(max_length=100)
    Vehicle_PlateNumber = models.CharField(max_length=10)
    Vehicle_Speed = models.IntegerField()
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)


class Fine(models.Model):
    fine = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10)
