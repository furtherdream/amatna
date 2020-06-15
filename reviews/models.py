from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review models definition """

    review = models.TextField(_("review"))
    rating = models.IntegerField(
        _("rating"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("restaurant"),
    )

    def __str__(self):
        return self.review

    class Meta:
        ordering = ("-created",)
        verbose_name = _("review")
        verbose_name_plural = _("reviews")
