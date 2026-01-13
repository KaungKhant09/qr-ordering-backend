from django.contrib import admin
from .models import Plan, ItemCategory, PlanCategoryAccess

# Register your models here.
admin.site.register(Plan)
admin.site.register(ItemCategory)
admin.site.register(PlanCategoryAccess)