from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from restaurants import models as restaurant_models
from . import forms


def create_review(request, restaurant):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        restaurant = restaurant_models.Restaurant.objects.get_or_none(pk=restaurant)
        if not restaurant:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            messages.success(request, _("Your review have been written"))
            return redirect(reverse("restaurants:detail", kwargs={"pk": restaurant.pk}))
