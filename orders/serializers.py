from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemCreateSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(required=False, allow_blank=True)

class OrderCreateSerializer(serializers.Serializer):
    qr_token = serializers.UUIDField()
    items = OrderItemCreateSerializer(many=True)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "created_at"]