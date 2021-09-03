import math
from datetime import datetime

import requests
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from need_gas_app.api.interactors import DriverInteractor, StationInteractor, drivers_url
from need_gas_app.api.serializers import (
    ClientSerializer,
    ServiceSerializer,
    DriverSerializer,
    RequestSerializer,
)
from need_gas_app.models import Service, Client, Driver, Request, ServiceStates


# List Clients
class ClientListAV(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Particular client details
class ClientDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# List services for a client
class ClientServiceListAV(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Service.objects.filter(client=pk)


# List all services or list by date
class ServiceListAV(APIView):
    def get(self, request):
        date = request.GET.get("date")
        if date:
            date = datetime.fromisoformat(date).date()
            services = Service.objects.filter(created_time__date=date)
        else:
            services = Service.objects.all()
        serializer = ServiceSerializer(
            services, many=True, context={"request": request}
        )
        return Response(serializer.data)


# Individual view for a service
class ServiceDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# Request service
class ServiceRequestAV(APIView):
    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            available_drivers = Driver.objects.filter(active=False).all()
            if not available_drivers:
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

            driver_interactor = DriverInteractor(available_drivers)
            station_interactor = StationInteractor()

            closest_driver, driver_dist = driver_interactor.get_nearest(client)
            closest_driver.active = True
            closest_driver.save()

            Service.objects.create(
                client=client, driver=closest_driver, state=ServiceStates.in_progress
            )

            closest_station, driver_to_station_dist = station_interactor.get_nearest(
                closest_driver
            )

            station_to_client_dist = math.dist(
                [client.x, client.y], [closest_station.x, closest_station.y]
            )

            total_dist = driver_to_station_dist + station_to_client_dist

            # assuming distances in kms
            total_minutes = 60 * total_dist / driver_interactor.speed_kmh
            total_minutes += driver_interactor.recharge_time

            ser = RequestSerializer(Request(closest_driver.id, total_minutes))
            return Response(ser.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Location-sorted List of drivers
class DriverListAV(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        if not drivers:
            return Response(status=status.HTTP_404_NOT_FOUND)
        x = int(request.GET.get("x", 0))
        y = int(request.GET.get("y", 0))
        driver_interactor = DriverInteractor(drivers)
        dist, closest = driver_interactor.kdtree.query([(x, y)], k=len(drivers))
        drivers = [Driver.objects.get(id=int(pk + 1)) for pk in closest[0]]
        serializer = DriverSerializer(drivers, many=True, context={"request": request})
        return Response(serializer.data)


# Particular driver details
class DriverDetailAV(generics.RetrieveUpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


# Triggered when driver arrives destination
class DriverArrivedAV(APIView):
    def post(self, request, pk):
        try:
            driver = Driver.objects.get(id=pk)
            driver.active = False
            driver.save()

            service = Service.objects.get(driver=driver)
            service.state = ServiceStates.finished
            service.save()
            serializer = DriverSerializer(driver, context={"request": request})
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Sync with drivers service
class DriverSyncAV(APIView):
    def get(self, request, *args, **kwargs):
        uptated_locations = requests.get(drivers_url).json()
        drivers = {d.get("id"): d for d in uptated_locations}
        for pk in drivers.keys():
            driver = drivers.get(pk)
            driver.pop("last-update")
            try:
                Driver.objects.get(id=pk)
                driver = Driver.objects.filter(id=pk).update(**driver)
                request_status = status.HTTP_200_OK
            except Driver.DoesNotExist:
                Driver.objects.create(**driver)
                request_status = status.HTTP_201_CREATED

        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True, context={"request": request})
        return Response(serializer.data, status=request_status)
