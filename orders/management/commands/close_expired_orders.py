from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order


class Command(BaseCommand):
    help = "Automatically close expired buffet orders"

    def handle(self, *args, **options):
        now = timezone.now()

        expired_orders = Order.objects.filter(
            status__in=["pending", "preparing", "served"],
            expires_at__lt=now,
        )

        count = expired_orders.update(status="closed")

        self.stdout.write(
            self.style.SUCCESS(f"Closed {count} expired orders.")
        )