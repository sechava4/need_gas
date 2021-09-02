from datetime import datetime

import requests
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

from need_gas_app.api.interactors import DriverInteractor
from need_gas_app.models import Service, Client, Driver
from need_gas_app.api.serializers import (
    ClientSerializer,
    ServiceSerializer,
    DriverSerializer,
    TaskSerializer,
)


class ClientListAV(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientServiceListAV(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Service.objects.filter(client=pk)


class ServiceListAV(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request):
        date = request.GET.get("date")
        if date:
            date = datetime.fromisoformat(date).date()
            services = Service.objects.filter(created_time__date=date)
        else:
            services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)


class ServiceDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceRequestAV(APIView):
    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            drivers = DriverInteractor()
            driver = drivers.get_nearest(client, 1)
            ser = TaskSerializer(driver)
            return Response(ser.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DriverListAV(APIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get(self, request):
        drivers = Driver.objects.all()
        x = int(request.GET.get("x", 0))
        y = int(request.GET.get("y", 0))
        driver_interactor = DriverInteractor(drivers)
        dist, closest = driver_interactor.kdtree.query([(x, y)], k=len(drivers))
        drivers = [Driver.objects.get(id=int(pk + 1)) for pk in closest[0]]
        serializer = DriverSerializer(drivers, many=True, context={'request': request})
        return Response(serializer.data)


class DriverSyncAV(APIView):
    def get(self, request, *args, **kwargs):
        uptated_locations = requests.get(DriverInteractor.drivers_url).json()
        drivers = {d.get("id"): d for d in uptated_locations}
        for pk in drivers.keys():
            driver = drivers.get(pk)
            driver.pop('last-update')
            try:
                Driver.objects.get(id=pk)
                driver = Driver.objects.filter(id=pk).update(**driver)
                request_status = status.HTTP_200_OK
            except Driver.DoesNotExist:
                Driver.objects.create(**driver)
                request_status = status.HTTP_201_CREATED

        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True, context={'request': request})
        return Response(serializer.data, status=request_status)
