from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from restaurants import models as restaurant_models
from . import models


def toggle_restaurant(request, restaurant_pk):
    action = request.GET.get("action", None)
    restaurant = restaurant_models.Restaurant.objects.get_or_none(pk=restaurant_pk)
    if restaurant is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(user=request.user)
        if action == "add":
            the_list.restaurants.add(restaurant)
        elif action == "remove":
            the_list.restaurants.remove(restaurant)

    return redirect(reverse("restaurants:detail", kwargs={"pk": restaurant_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"

