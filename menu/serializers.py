from rest_framework import serializers
from .models import Menu, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual menu items.
    Controls what the frontend sees.
    """

    class Meta:
        model = MenuItem
        fields = ["id", "name", "description"]

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for menu with nested menu items.
    """

    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "items"]