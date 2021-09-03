from abc import ABC

from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from need_gas_app.models import Service, Client, Driver


class ServiceSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ClientSerializer(EnumSupportSerializerMixin, serializers.HyperlinkedModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class RequestSerializer(serializers.Serializer):
    driver_id = serializers.IntegerField()
    minutes = serializers.FloatField()
