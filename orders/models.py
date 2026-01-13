from django.db import models
from tables.models import Table
from menu.models import MenuItem

# Create your models here.
class Order(models.Model):
    """
    Represents a single customer order session.

    One table can have multiple orders over time.
    Orders are append-only in MVP.
    """

    # Controlled list of valid order states
    STATUS_CHOICES = [
        ("pending", "Pending"),        # Order placed by customer
        ("preparing", "Preparing"),    # Kitchen acknowledged
        ("served", "Served"),          # Delivered to table
        ("closed", "Closed"),          # Finished / paid / expired
    ]

    # Which table placed the order
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE
    )

    # Current lifecycle state of the order
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Timestamp when the order was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"

class OrderItem(models.Model):
    """
    Represents one line item inside an Order.
    Example: 2x Beef Slice.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    # Optional customer notes (e.g. 'no spicy')
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"