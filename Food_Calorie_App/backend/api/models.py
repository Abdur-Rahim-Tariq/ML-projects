from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories_per_100g = models.FloatField()

    def __str__(self):
        return self.name

class CalorieRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    servings = models.FloatField()
    weight_in_grams = models.FloatField()
    total_calories = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item}"
