from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("upload/", views.upload_image),
    path('save_record/', views.save_record),
    path("save/", views.save_record),
    path("records/", views.get_records),
    path("delete/<int:record_id>/", views.delete_record),
    path("summary/", views.calorie_summary),
]



def home(request):
    return HttpResponse("<h1>Welcome to Food Calorie App Backend 🚀</h1>")
