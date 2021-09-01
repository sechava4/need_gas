from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from need_gas_app.models import Service, Client
from need_gas_app.api.serializers import ClientSerializer, ServiceSerializer


@api_view(http_method_names=['GET'])
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET', 'POST'])
def services_list(request):
    if request.method == 'GET':
        today = datetime.today()
        date = request.GET.get("date", today)
        services = Service.objects.filter(created_time=date).all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


