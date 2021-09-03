import dataclasses
from enum import Enum
from enumfields import EnumField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ServiceStates(Enum):
    finished = "finished"
    in_progress = "in_progress"
    not_started = "not_started"


class Client(models.Model):
    name = models.CharField(max_length=30)
    x = models.FloatField(max_length=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    y = models.FloatField(max_length=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated = models.DateTimeField(auto_now=True)


class Driver(models.Model):
    id = models.IntegerField(primary_key=True)
    x = models.FloatField(max_length=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    y = models.FloatField(max_length=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)


class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="services")
    state = EnumField(ServiceStates, max_length=15)
    created_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@dataclasses.dataclass
class Station:
    id: int
    x: float
    y: float


@dataclasses.dataclass
class Request:
    driver_id: int
    minutes: float
