from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("<int:pk>/", views.RestaurantDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
    path("channel/<int:pk>/", views.channel_view, name="channel"),
]
