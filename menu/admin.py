from django.contrib import admin
from .models import Menu, MenuItem

# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Improves admin usability for Menu Items.
    """

    # Columns shown in the list view
    list_display = ("name", "category", "menu", "is_active")

    # Enables filtering by category and menu
    list_filter = ("category", "menu", "is_active")

    # Enables search by item name
    search_fields = ("name",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "is_active")
