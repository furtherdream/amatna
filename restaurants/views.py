import io
import csv
from django.shortcuts import render, reverse
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from reviews import forms as review_forms
from django.contrib import messages
from . import models


def main_views(request):
    channel_ranked = models.Channel.objects.all().order_by("rank")[0:8]
    all_categories = models.Category.objects.all().order_by("created")
    page = request.GET.get("page")
    all_restaurant = models.Restaurant.objects.all().order_by("-created")[0:80]
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
    return render(
        request,
        "restaurants/channel_view.html",
        {"channels": channels},
    )


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


def search_channels(request):
    channel_name = request.GET.get("search_channel")
    page = request.GET.get("page")
    qs = models.Channel.objects.filter(name__contains=channel_name)
    paginator = Paginator(qs, 40)
    channels = paginator.get_page(page)
    return render(
        request,
        "restaurants/channel_view.html",
        {
            "channels": channels,
            "channel_name": channel_name
        },
    )


def search(request):
    tag = request.GET.get("tag_set")
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(
        tag_set__name__contains=tag).order_by("-created")
    paginator = Paginator(qs, 100)
    restaurants = paginator.get_page(page)
    return render(
        request,
        "restaurants/search.html",
        {
            "tag": tag,
            "restaurants": restaurants
        },
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
        {
            "channel": channel,
            "restaurants": restaurants
        },
    )


def category_search(request, pk):
    all_categories = models.Category.objects.all().order_by("created")
    category = models.Category.objects.get(pk=pk)
    page = request.GET.get("page")
    qs = models.Restaurant.objects.filter(category__pk=pk).order_by("-created")
    paginator = Paginator(qs, 100)
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


def restaurant_upload(request):
    # declaring template
    template = "restaurants/restaurant_upload.html"
    prompt = {
        "order":
            "Order of the CSV should be name, blog_count, biztel, address, menu_list"
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line
    # we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter='|', quotechar='"'):
        restaurant, created = models.Restaurant.objects.update_or_create(
            naver_place_id=column[1])
        restaurant.save()
        channel = models.Channel.objects.filter(name=column[0])
        for id in channel:
            restaurant.channel.add(id)
        youtube = models.Youtube.objects.filter(video_id=column[2])
        for id in youtube:
            restaurant.youtube.add(id)

    return render(request, template)


def youtube_upload(request):
    # declaring template
    template = "restaurants/youtube_upload.html"
    # prompt is a context variable that can have different values
    # depending on their context
    prompt = {"order": "Order of the CSV should be name, title, video_id"}
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line
    # we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter='|', quotechar='"'):
        youtube, created = models.Youtube.objects.update_or_create(
            video_id=column[0],
            name=column[1],
        )

    return render(request, template)
