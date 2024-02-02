from django.contrib import admin
from .models import Owner, Vehicle, Junction

admin.site.register(Owner)
admin.site.register(Junction)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('PlateNumber', 'Owner', 'Color', 'VType',)
    list_filter = ('Color', 'VType')

admin.site.register(Vehicle, VehicleAdmin)
