from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tables.models import Table
from menu.models import MenuItem
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer

# Create your views here.
class CreateOrderView(APIView):
    """
    Create a new order from QR token and items list.
    """

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qr_token = serializer.validated_data["qr_token"]
        items = serializer.validated_data["items"]

        try:
            table = Table.objects.get(qr_token=qr_token, is_active=True)
        except Table.DoesNotExist:
            return Response(
                {"error": "Invalid QR code"},
                status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.create(table=table)

        for item in items:
            menu_item = MenuItem.objects.get(id=item["menu_item_id"])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item["quantity"],
                note=item.get("note", "")
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class StaffOrderListView(APIView):
    """
    List all active (non-closed) orders.
    """

    def get(self, request):
        orders = Order.objects.exclude(status="closed")
        data = OrderSerializer(orders, many=True).data
        return Response(data)

class UpdateOrderStatusView(APIView):
    """
    Update order status (staff action).
    """

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        status_value = request.data.get("status")
        order.status = status_value
        order.save()

        return Response(OrderSerializer(order).data)