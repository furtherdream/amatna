from django.urls import path
from restaurants import views as restaurant_views
from django.views.generic import TemplateView

app_name = "core"
# include() 안에 namespace 를 사용하면 app_name 을 지정해 줘야 한다.(namespace = app_name)

urlpatterns = [
    path("", restaurant_views.main_views, name="home"),
    path(
        'robots.txt/',
        TemplateView.as_view(
            template_name="robots.txt", content_type='text/plain')),
]
