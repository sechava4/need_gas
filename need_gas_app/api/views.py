from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from need_gas_app.models import Service, Client
from need_gas_app.api.serializers import ClientSerializer, ServiceSerializer


class ClientListAV(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ServiceListAV(APIView):
    def get(self, request):
        today = datetime.today()
        date = request.GET.get("date", today)
        services = Service.objects.filter(created_time=date).all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailAV(APIView):
    def get(self, request, pk):
        try:
            service_model = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service_model)
        return Response(serializer.data)

    def put(self, request, pk):
        service_model = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        service_model = Service.objects.get(pk=pk)
        service_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


