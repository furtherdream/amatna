from django.contrib import admin
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

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
