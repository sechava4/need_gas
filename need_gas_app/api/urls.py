from django.urls import path
from need_gas_app.api.views import (
    ClientListAV,
    ServiceListAV,
    ServiceDetailAV,
)

urlpatterns = [
    path('clients/', ClientListAV.as_view(), name='client-list'),
    path('services/', ServiceListAV.as_view(), name='services-list'),
    path('services/<int:pk>', ServiceDetailAV.as_view(), name='service-detail'),
]
