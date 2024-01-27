from django.urls import path
from .views import (register_owner, register_junction)

urlpatterns = [
    path('register_owner', register_owner, name='register_owner'),
    path('register_junction', register_junction, name='register_junction')

]