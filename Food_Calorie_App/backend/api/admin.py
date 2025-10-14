from django.contrib import admin
from .models import FoodItem
# Register your models here.

from django.contrib import admin
from .models import FoodItem

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "calories_per_100g")

