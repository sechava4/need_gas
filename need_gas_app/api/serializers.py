from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers
from need_gas_app.models import Service, Client


class ServiceSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ClientSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = '__all__'
