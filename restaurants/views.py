from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from django.core.paginator import Paginator
from . import models


def main_views(request):
    all_channels = models.Channel.objects.all().order_by("rank")[0:8]
    page = request.GET.get("page")
    all_restaurant = models.Restaurant.objects.all().order_by("-created")
    paginator = Paginator(all_restaurant, 16)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/main.html",
        context={"channels": all_channels, "restaurants": restaurants},
    )


class RestaurantDetail(DetailView):

    """ Restaurant Detail Definition """

    model = models.Restaurant


def search(request):
    tag = request.GET.get("tag_set")
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(tag_set__name=tag).order_by("-created")
    paginator = Paginator(qs, 40)
    restaurants = paginator.get_page(page)
    return render(
        request, "restaurants/search.html", {"tag": tag, "restaurants": restaurants},
    )


def channel_view(request, pk):
    channel = models.Channel.objects.get(pk=pk)
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(channel__pk=pk).order_by("-created")
    paginator = Paginator(qs, 100)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/search.html",
        {"channel": channel, "restaurants": restaurants},
    )


def category_search(request, pk):
    category = models.Category.objects.get(pk=pk)
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(category__pk=pk).order_by("-created")
    paginator = Paginator(qs, 40)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/search.html",
        {"category": category, "restaurants": restaurants},
    )
