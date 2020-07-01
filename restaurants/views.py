from django.shortcuts import render, reverse
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from reviews import forms as review_forms
from . import models


def main_views(request):
    channel_ranked = models.Channel.objects.all().order_by("rank")[0:8]
    all_categories = models.Category.objects.all().order_by("created")
    page = request.GET.get("page")
    all_restaurant = models.Restaurant.objects.all().order_by("-created")
    paginator = Paginator(all_restaurant, 16)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/main.html",
        context={
            "channels": channel_ranked,
            "restaurants": restaurants,
            "all_categories": all_categories,
        },
    )


def channel_view(request):
    page = request.GET.get("page")
    all_channel = models.Channel.objects.all().order_by("-created")
    paginator = Paginator(all_channel, 16)
    channels = paginator.get_page(page)
    return render(request, "restaurants/channel_view.html", {"channels": channels},)


class RestaurantDetail(DetailView, FormMixin):

    """ Restaurant Detail Definition """

    model = models.Restaurant
    form_class = review_forms.CreateReviewForm

    def get_success_url(self):
        return reverse("restaurants:detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context["form"] = review_forms.CreateReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(RestaurantDetail, self).form_valid(form)


def search(request):
    tag = request.GET.get("tag_set")
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(tag_set__name=tag).order_by("-created")
    paginator = Paginator(qs, 40)
    restaurants = paginator.get_page(page)
    return render(
        request, "restaurants/search.html", {"tag": tag, "restaurants": restaurants},
    )


def channel_search(request, pk):
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
    all_categories = models.Category.objects.all().order_by("created")
    category = models.Category.objects.get(pk=pk)
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(category__pk=pk).order_by("-created")
    paginator = Paginator(qs, 40)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/search.html",
        {
            "category": category,
            "restaurants": restaurants,
            "all_categories": all_categories,
        },
    )
