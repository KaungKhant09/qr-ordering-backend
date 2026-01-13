from django.db import models
from restaurants.models import Restaurant
import uuid 

# Create your models here.
class Table(models.Model):
    """
    Represents a physical table inside a restaurant.

    Each table is identified by a QR code.
    The QR code maps to `qr_token`, NOT the table ID.
    """

    # Which restaurant this table belongs to
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    # Table identifier shown to customers (e.g. "A1", "12", "VIP-3")
    table_number = models.CharField(max_length=50)

    # Random, unguessable token embedded in the QR code
    # This is what the frontend sends to the backend
    qr_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    # Allows disabling a table without deleting history
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - Table {self.table_number}"