from django.db import models
from restaurants.models import Restaurant
from plans.models import ItemCategory


class Menu(models.Model):
    """
    Represents a menu configuration for a restaurant.

    NOTE:
    - Menu is NOT a buffet plan.
    - Menu is a catalog container for menu items.
    - Buffet rules live in the Plan model.
    """

    # Which restaurant this menu belongs to
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    # Display name shown to customers
    # Example: "Main Menu"
    name = models.CharField(max_length=255)

    # Allows seasonal or temporary menus
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Represents a single orderable item.

    Examples:
    - Beef Slice (Standard Meat)
    - Shrimp (Seafood)
    - Mala Spicy Soup (Soup Base)

    Each MenuItem belongs to exactly ONE category.
    """

    # Menu this item belongs to (catalog grouping)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # Display name shown to customers
    name = models.CharField(max_length=255)

    # Optional description for frontend display
    description = models.TextField(blank=True)

    # NEW: category for rule enforcement
    # Nullable only during Phase A for safe migration
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Controls visibility without deleting history
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name