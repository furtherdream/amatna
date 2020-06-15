from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Channel, models.Category, models.Tag)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.restaurant.count()


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    """ Restaurant Admin Definition """

    fieldsets = (
        (
            _("BasicInfo"),
            {
                "fields": (
                    "title",
                    "address",
                    "phone_number",
                    "price",
                    "biztime",
                    "breaktime",
                    "menu",
                    "holiday",
                )
            },
        ),
        (_("Media"), {"fields": ("youtube_id", "instagram_url",)}),
        (_("SortOfRestaurant"), {"fields": ("channel", "category", "tag_set",)},),
    )

    list_display = (
        "title",
        "youtube_id",
        "instagram_url",
        "address",
        "phone_number",
        "price",
        "biztime",
        "breaktime",
        "menu",
        "holiday",
    )

    list_filter = (
        "channel",
        "category",
        "tag_set",
    )

    filter_horizontal = (
        "channel",
        "category",
        "tag_set",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
