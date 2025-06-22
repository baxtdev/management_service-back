from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']


class OrderSerializer(WritableNestedModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
