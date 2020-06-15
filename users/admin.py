from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from reviews.models import Review
from . import models


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    inlines = (ReviewInline,)

    fieldsets = (
        (
            _("Custom Profile"),
            {
                "fields": (
                    (
                        "avatar",
                        "nickname",
                        "login_method",
                        "email_verified",
                        "email_secret",
                    )
                )
            },
        ),
    ) + UserAdmin.fieldsets

    list_display = (
        "username",
        "nickname",
        "email_verified",
        "email_secret",
        "login_method",
    )
    list_filter = ("login_method",)
