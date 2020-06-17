from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator
from . import models


def main_views(request):
    all_channels = models.Channel.objects.all()
    page = request.GET.get("page")
    all_restaurant = models.Restaurant.objects.all().order_by("-created")
    paginator = Paginator(all_restaurant, 1)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/restaurant_list.html",
        context={"channels": all_channels, "restaurants": restaurants},
    )


class RestaurantDetail(DetailView):

    """ Restaurant Detail Definition """

    model = models.Restaurant


def search(request):
    tag = request.GET.get("tag_set")
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(tag_set__name=tag).order_by("-created")
    paginator = Paginator(qs, 1)
    restaurants = paginator.get_page(page)

    return render(
        request, "restaurants/search.html", {"tag": tag, "restaurants": restaurants},
    )
