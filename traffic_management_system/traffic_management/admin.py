from django.contrib import admin
from .models import Owner, Vehicle, Junction

admin.site.register(Owner)
admin.site.register(Junction)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('Number', 'Owner', 'Color', 'Producer', 'Type', 'Year')
    list_filter = ('Color', 'Producer', 'Type', 'Year')

admin.site.register(Vehicle, VehicleAdmin)
