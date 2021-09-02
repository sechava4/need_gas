from django.urls import path
from need_gas_app.api.views import (
    ClientListAV,
    ClientDetailAV,
    ServiceListAV,
    ClientServiceListAV,
    ServiceDetailAV,
    ServiceRequestAV,
    DriverListAV,
    DriverSyncAV,
)

urlpatterns = [
    path('clients/', ClientListAV.as_view(), name='client-list'),
    path('clients/<int:pk>', ClientDetailAV.as_view(), name='client-detail'),
    path('clients/<int:pk>/request/', ServiceRequestAV.as_view(), name='client-request-service'),
    path('clients/<int:pk>/services/', ClientServiceListAV.as_view(), name='client-services'),
    path('services/', ServiceListAV.as_view(), name='services-list'),
    path('services/<int:pk>', ServiceDetailAV.as_view(), name='service-detail'),
    path('drivers/', DriverListAV.as_view(), name='driver-list'),
    path('drivers/sync', DriverSyncAV.as_view(), name='driver-list'),
]
