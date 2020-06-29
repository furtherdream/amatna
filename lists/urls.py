from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("add/<int:restaurant_pk>", views.save_restaurant, name="save-restaurant")
]
