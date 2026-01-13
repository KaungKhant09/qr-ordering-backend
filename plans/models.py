from django.db import models

# Create your models here.
class Plan(models.Model):
    """
    Buffet plan purchased by a customer.
    Defines time limit and allowed item categories.
    """
    name = models.CharField(max_length=50, unique=True)
    duration_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} min)"


class ItemCategory(models.Model):
    """
    Logical grouping for menu items.
    Examples: Soup Base, Standard Meat, Seafood.
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Item category"
        verbose_name_plural = "Item categories"

    def __str__(self):
        return self.name


class PlanCategoryAccess(models.Model):
    """
    Junction table defining which categories
    are allowed under which plan.
    """
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="allowed_categories",
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("plan", "category")

    def __str__(self):
        return f"{self.plan.name} → {self.category.name}"