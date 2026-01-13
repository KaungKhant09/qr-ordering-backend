from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tables.models import Table
from .models import Menu
from .serializers import MenuSerializer

# Create your views here.
class MenuByQRView(APIView):
    """
    Given a QR token, return the active menu and its items.
    """

    def get(self, request, qr_token):
        try:
            table = Table.objects.get(qr_token=qr_token, is_active=True)
        except Table.DoesNotExist:
            return Response(
                {"error": "Invalid QR code"},
                status=status.HTTP_404_NOT_FOUND
            )

        menu = Menu.objects.filter(
            restaurant=table.restaurant,
            is_active=True
        ).first()

        if not menu:
            return Response(
                {"error": "No active menu"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(MenuSerializer(menu).data)

