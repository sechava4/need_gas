from enum import Enum
from enumfields import EnumField

from django.db import models


class ServiceStates(Enum):
    finished = "finished"
    in_progress = "in_progress"
    not_started = "not_started"


class Client(models.Model):
    x = models.FloatField(max_length=5)
    y = models.FloatField(max_length=5)


class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="services")
    state = EnumField(ServiceStates, max_length=15)
    created_time = models.DateField(auto_now_add=True)


