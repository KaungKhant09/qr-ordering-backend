from django.urls import path
from .views import (
    CreateOrderView,
    StaffOrderListView,
    UpdateOrderStatusView,
)

urlpatterns = [
    path("orders/", CreateOrderView.as_view()),
    path("staff/orders/", StaffOrderListView.as_view()),
    path("staff/orders/<int:order_id>/status/", UpdateOrderStatusView.as_view()),
]