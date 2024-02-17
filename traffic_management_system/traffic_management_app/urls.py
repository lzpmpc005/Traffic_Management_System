from django.urls import path


from .views import (register_owner, register_junction, register_vehicle, logging,
                    payFine, retrieveReport, register_route)

urlpatterns = [
    path('register_owner', register_owner, name='register_owner'),
    path('register_junction', register_junction, name='register_junction'),
    path('register_vehicle', register_vehicle, name='register_vehicle'),
    path('logging', logging, name='logging'),
    path('payfine', payFine, name='payfine'),
    path('report', retrieveReport, name='retrieveReport'),
    path('register_route', register_route, name='register_route')
]