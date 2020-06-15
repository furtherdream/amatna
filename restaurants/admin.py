from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from . import models


@admin.register(models.Channel, models.Category, models.Tag)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.restaurant.count()


class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 1


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    """ Restaurant Admin Definition """

    inlines = (PhotoInline,)

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
        "total_rating",
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

    search_fields = ("title", "youtube_id")


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="75px" src="{obj.file.url}" />')

    get_thumbnail.short_description = _("thumbnail")
