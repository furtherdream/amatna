from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator
from . import models


def main_views(request):
    all_channels = models.Channel.objects.all()
    page = request.GET.get("page")
    all_restaurant = models.Restaurant.objects.all().order_by("-created")
    paginator = Paginator(all_restaurant, 20)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/home.html",
        context={"channels": all_channels, "restaurants": restaurants},
    )


class RestaurantDetail(DetailView):

    """ Restaurant Detail Definition """

    model = models.Restaurant
