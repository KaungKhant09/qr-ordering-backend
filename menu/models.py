from django.db import models
from restaurants.models import Restaurant

# Create your models here.
class Menu(models.Model):
    """
    Represents a menu configuration (e.g. Buffet Plan).
    This does NOT contain individual food items yet.
    That comes later.
    """

    # Which restaurant this menu belongs to
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    # Display name shown to customers
    # Example: "Standard Buffet", "Premium Buffet"
    name = models.CharField(max_length=255)

    # Allows seasonal or temporary menus
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    """
    Represents a single orderable item under a Menu.
    Example: 'Beef Slice', 'Shrimp', 'Mushroom'.
    """

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(max_length=255)

    # Optional description for frontend display
    description = models.TextField(blank=True)

    # Controls visibility without deleting history
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name