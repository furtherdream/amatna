from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [path("create/<int:restaurant>", views.create_review, name="create")]
