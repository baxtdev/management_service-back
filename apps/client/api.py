from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import Client,ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    