from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from . import models


@admin.register(models.Channel, models.Category, models.Tag, models.Youtube)
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
                    "menu",
                    "naver_place_id",
                    "blog_count",
                    "tv_list",
                )
            },
        ),
        (_("ByTyping"), {"fields": (
            "price",
            "biztime_start",
            "biztime_end",
            "biztime_24",
            "biztime_desc",
            "breaktime",
            "holiday",
            "info",
            "comment",
            "category",
            "tag_set",
            "instagram_url",
        )}),
        (_("Media"), {"fields": ("channel", "youtube",)}),
    )

    list_display = (
        "title",
        "address",
        "phone_number",
        "price",
        "biztime_start",
        "biztime_end",
        "biztime_24",
        "breaktime",
        "menu",
        "holiday",
    )

    list_filter = (
        "channel",
        "category",
        "tag_set",
    )

    filter_horizontal = ("channel", "category", "tag_set", "youtube")

    search_fields = ("title",)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="75px" src="{obj.file.url}" />')

    get_thumbnail.short_description = _("thumbnail")
