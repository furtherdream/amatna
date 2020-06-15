from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class List(core_models.TimeStampedModel):

    """ List Model Definition """

    class Meta:
        verbose_name = _("list")
        verbose_name_plural = _("lists")

    user = models.OneToOneField(
        "users.User",
        related_name="list",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    restaurants = models.ManyToManyField(
        "restaurants.Restaurant",
        related_name="lists",
        blank=True,
        verbose_name=_("restaurant"),
    )

    def count_restaurants(self):
        return self.restaurants.count()

    count_restaurants.short_description = _("Number of Restaurants")
