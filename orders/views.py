from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from datetime import timedelta

from tables.models import Table
from menu.models import MenuItem
from plans.models import Plan
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer


class CreateOrderView(APIView):
    """
    Create a new order from QR token, plan, and items list.

    ENFORCEMENT (Phase C):
    - Order must have a plan
    - Buffet timing is auto-calculated
    - Menu items must be allowed under the selected plan
    """

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qr_token = serializer.validated_data["qr_token"]
        plan_id = serializer.validated_data["plan_id"]
        items = serializer.validated_data["items"]

        # 1️⃣ Validate table from QR
        try:
            table = Table.objects.get(qr_token=qr_token, is_active=True)
        except Table.DoesNotExist:
            return Response(
                {"error": "Invalid QR code"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Validate plan
        try:
            plan = Plan.objects.get(id=plan_id, is_active=True)
        except Plan.DoesNotExist:
            return Response(
                {"error": "Invalid or inactive plan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Set buffet timing
        started_at = timezone.now()
        expires_at = started_at + timedelta(minutes=plan.duration_minutes)

        # 4️⃣ Create order
        order = Order.objects.create(
            table=table,
            plan=plan,
            started_at=started_at,
            expires_at=expires_at,
        )

        # 5️⃣ Fetch allowed category IDs for this plan
        allowed_category_ids = set(
            plan.allowed_categories.values_list("category_id", flat=True)
        )

        # 6️⃣ Validate and create order items
        for item in items:
            try:
                menu_item = MenuItem.objects.get(
                    id=item["menu_item_id"],
                    is_active=True
                )
            except MenuItem.DoesNotExist:
                return Response(
                    {"error": "Invalid menu item"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ❌ Reject item not allowed by plan
            if menu_item.category_id not in allowed_category_ids:
                return Response(
                    {
                        "error": (
                            f"Item '{menu_item.name}' is not allowed "
                            f"under the {plan.name} plan."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

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