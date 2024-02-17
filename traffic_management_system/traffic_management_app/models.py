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
    PlateNumber = models.OneToOneField(Plates, null=True, on_delete=models.SET_NULL)


class Junction(models.Model):
    Address = models.CharField(max_length=100)
    JType = models.CharField(max_length=20)
    Light = models.IntegerField(default=1)


class Log(models.Model):
    Junction = models.ForeignKey(Junction, null=True, on_delete=models.SET_NULL)
    Vehicle_PlateNumber = models.CharField(max_length=10)
    Vehicle_Speed = models.IntegerField()
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)


class Fine(models.Model):
    fine = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)


class DriverLicense(models.Model):
    Owner = models.OneToOneField(Owner, on_delete=models.SET_NULL, null=True)
    License_Number = models.CharField(max_length=10)
    Issue_Date = models.DateField(auto_now_add=True)
    Expire_Date = models.CharField(default="LifeLong")
    Status = models.CharField(max_length=10, default='Valid')
    Score = models.IntegerField(default=12)


class StatReport(models.Model):
    Junction = models.ForeignKey(Junction, on_delete=models.CASCADE, null=False)
    Vehicle_Quantity = models.IntegerField(default=1)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField()


class Street(models.Model):
    Start_junction = models.ForeignKey(Junction, on_delete=models.CASCADE, null=False, related_name='start_junction')
    End_junction = models.ForeignKey(Junction, on_delete=models.CASCADE, null=False, related_name='end_junction')
    Distance = models.IntegerField()
    Name = models.CharField(max_length=50)

