from django.urls import path
from restaurants import views as restaurant_views

app_name = "core"
# include() 안에 namespace 를 사용하면 app_name 을 지정해 줘야 한다.(namespace = app_name)

urlpatterns = [path("", restaurant_views.main_views, name="home")]
