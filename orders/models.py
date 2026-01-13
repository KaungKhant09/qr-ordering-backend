from django.db import models
from tables.models import Table
from menu.models import MenuItem
from plans.models import Plan


class Order(models.Model):
    """
    Represents a single customer order session.

    NEW CONCEPT (Phase A):
    - Each order is tied to a buffet Plan.
    - Plan determines time limit and allowed item categories.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),        # Order placed by customer
        ("preparing", "Preparing"),    # Kitchen acknowledged
        ("served", "Served"),          # Delivered to table
        ("closed", "Closed"),          # Finished / expired
    ]

    # Which table placed the order
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE
    )

    # NEW: buffet plan selected by the customer
    # Nullable for Phase A to allow safe migration
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Current lifecycle state of the order
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # NEW: timing fields (not enforced yet)
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the buffet session started"
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the buffet session expires"
    )

    # Timestamp when the order record was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"


class OrderItem(models.Model):
    """
    Represents one line item inside an Order.

    NOTE:
    - Validation against Plan rules will be added in Phase C.
    - For now, this remains unchanged.
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