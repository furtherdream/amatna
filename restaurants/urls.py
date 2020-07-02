from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("<int:pk>/", views.RestaurantDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
    path("search-channels/", views.search_channels, name="search-channels"),
    path("channel/", views.channel_view, name="channels"),
    path("channel/<int:pk>/", views.channel_search, name="channel"),
    path("category/<int:pk>/", views.category_search, name="category"),
]
