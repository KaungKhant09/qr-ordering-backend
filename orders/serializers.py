from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Represents a single item in an order request.
    """
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(required=False, allow_blank=True)


class OrderCreateSerializer(serializers.Serializer):
    """
    Payload used by customers to create an order.
    """
    qr_token = serializers.UUIDField()
    plan_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer used for responses (customer + staff).
    """
    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "started_at",
            "expires_at",
            "created_at",
        ]