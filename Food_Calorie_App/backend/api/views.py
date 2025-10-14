from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ultralytics import YOLO
from .models import CalorieRecord, FoodItem
from datetime import date, timedelta
import os

model = YOLO("./best.pt") 

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if not username or not password or not email:
        return Response({"error": "Username, email, and password are required."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"message": "User created successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)
    return Response({"message": "Login successful", "username": user.username})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    image = request.FILES.get("image")
    if not image:
        return Response({"error": "No image uploaded"}, status=400)

    temp_path = "temp.jpg"
    with open(temp_path, "wb+") as f:
        for chunk in image.chunks():
            f.write(chunk)

    results = model.predict(temp_path)
    detected_items = []

    for result in results:
        if result.boxes is not None:
            for cls_idx in result.boxes.cls:
                detected_items.append(result.names[int(cls_idx)])

    os.remove(temp_path)
    return Response({"detected_items": list(set(detected_items))})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_record(request):
    user = request.user
    data = request.data  # Expecting: {"items": [{"food_item": "Pizza", "servings": 2, "weight_in_grams": 150}]}

    saved_items = []

    for item in data.get("items", []):
        food_name = item.get("food_item")
        servings = float(item.get("servings", 1))
        weight_in_grams = float(item.get("weight_in_grams", 100))

        # Lookup food item from database
        try:
            food = FoodItem.objects.get(name__iexact=food_name)
        except FoodItem.DoesNotExist:
            return Response({"error": f"Food item '{food_name}' not found in database"}, status=400)

        # Calculate total calories
        total_calories = (food.calories_per_100g * weight_in_grams / 100) * servings

        # Save record
        record = CalorieRecord.objects.create(
            user=user,
            food_item=food.name,
            servings=servings,
            weight_in_grams=weight_in_grams,
            total_calories=total_calories
        )

        saved_items.append({
            "food_item": food.name,
            "servings": servings,
            "weight_in_grams": weight_in_grams,
            "total_calories": total_calories
        })

    return Response({
        "message": "Calorie records saved successfully!",
        "saved_items": saved_items
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_records(request):
    tab = request.query_params.get("tab", "daily")  # daily / weekly / monthly
    today = date.today()

    if tab == "daily":
        start_date = today
    elif tab == "weekly":
        start_date = today - timedelta(days=today.weekday())  # start of week
    elif tab == "monthly":
        start_date = today.replace(day=1)
    else:
        start_date = None

    records = CalorieRecord.objects.filter(user=request.user)
    if start_date:
        records = records.filter(date__gte=start_date)

    data = [
        {
            "id": r.id,
            "food_item": r.food_item,
            "servings": r.servings,
            "weight_in_grams": r.weight_in_grams,
            "total_calories": r.total_calories,
            "date": r.date
        } for r in records
    ]
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_record(request, record_id):
    CalorieRecord.objects.filter(id=record_id, user=request.user).delete()
    return Response({"message": "Record deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calorie_summary(request):
    today = date.today()
    daily = sum(r.total_calories for r in CalorieRecord.objects.filter(user=request.user, date=today))
    monthly = sum(r.total_calories for r in CalorieRecord.objects.filter(user=request.user, date__month=today.month))
    return Response({"daily": daily, "monthly": monthly})


def home(request):
    return HttpResponse("<h1>Welcome to Food Calorie App Backend 🚀</h1>")


