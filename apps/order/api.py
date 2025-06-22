from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend


from .serializers import Order,OrderSerializer,OrderListSerializer,\
                        OrderItem,OrderItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status','customer','date']
    

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return OrderListSerializer
        return super().get_serializer_class()

