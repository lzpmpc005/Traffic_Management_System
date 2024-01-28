from django.urls import path


from .views import (register_owner, register_junction, register_vehicle, recognize_vehicle)

urlpatterns = [
    path('register_owner', register_owner, name='register_owner'),
    path('register_junction', register_junction, name='register_junction'),

    path('register_vehicle', register_vehicle, name='register_vehicle'),
    path('recognize_vehicle', recognize_vehicle, name='recognize_vehicle')
]