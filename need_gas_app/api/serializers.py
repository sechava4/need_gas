from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers
from need_gas_app.models import Service, Client


class ServiceSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        return Service.objects.create(**validated_data)


class ClientSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
