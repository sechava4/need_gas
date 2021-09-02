from django.contrib import admin
from need_gas_app.models import Client, Service, Driver

# Register your models here.
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Driver)
