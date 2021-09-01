from django.urls import path
from need_gas_app.api.views import client_list, services_list

urlpatterns = [
    path('clients/', client_list, name='client-list'),
    path('services/', services_list, name='services-list'),
]
