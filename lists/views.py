from django.shortcuts import render, redirect, reverse
from restaurants import models as restaurant_models
from . import models


def save_restaurant(request, restaurant_pk):
    restaurant = restaurant_models.restaurant.objects.get_or_none(pk=restaurant_pk)
    if restaurant is not None:
        the_list, _ = models.List.objects.get_or_create(user=request.user,)
        the_list.restaurants.add(restaurant)

    return redirect(reverse("restaurants:detail", kwargs={"pk": restaurant_pk}))
