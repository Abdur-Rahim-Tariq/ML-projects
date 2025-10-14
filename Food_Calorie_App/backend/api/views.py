from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ultralytics import YOLO
from .models import CalorieRecord, FoodItem
from datetime import date
import os

model = YOLO("./best.pt") 
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")  # make sure you get email

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
    data = request.data
    for item in data.get("items", []):
        CalorieRecord.objects.create(
            user=user,
            food_item=item["food_item"],
            servings=item["servings"],
            weight_in_grams=item["weight_in_grams"],
            total_calories=item["total_calories"]
        )
    return Response({"message": "Record saved successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_records(request):
    records = CalorieRecord.objects.filter(user=request.user)
    data = [
        {
            "id": r.id,
            "food_item": r.food_item,
            "servings": r.servings,
            "weight": r.weight_in_grams,
            "calories": r.total_calories,
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
