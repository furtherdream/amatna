from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [path("<int:pk>", views.RestaurantDetail.as_view(), name="detail")]
