from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path(
        "toggle/<int:restaurant_pk>/", views.toggle_restaurant, name="toggle-restaurant"
    ),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]
