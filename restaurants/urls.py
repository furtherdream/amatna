from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("<int:pk>/", views.RestaurantDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
    path("search-channels/", views.search_channels, name="search-channels"),
    path("channel/", views.channel_view, name="channels"),
    path("channel/<str:verb>/", views.channel_search, name="channel"),
    path("category/<str:verb>/", views.category_search, name="category"),
    path(
        'r_upload-with-csv/', views.restaurant_upload,
        name="restaurant-upload"),
    path('y_upload-with-csv/', views.youtube_upload, name="youtube-upload"),
]
