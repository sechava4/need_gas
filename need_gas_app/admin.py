from django.contrib import admin
from need_gas_app.models import Client, Service, Driver

# Model registration
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Driver)
