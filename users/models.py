from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):

    """ Custom User Model """

    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"
    LOGIN_FACEBOOK = "facebook"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("Email")),
        (LOGIN_KAKAO, _("Kakao")),
        (LOGIN_NAVER, _("Naver")),
        (LOGIN_FACEBOOK, _("Facebook")),
    )

    avatar = models.ImageField(_("avatar"), upload_to="avatars", blank=True)
    nickname = models.CharField(_("nickname"), max_length=20, default="")
    email_verified = models.BooleanField(_("email verified"), default=False)
    email_secret = models.CharField(
        _("email secret"), max_length=20, default="", blank=True
    )
    login_method = models.CharField(
        _("login method"), choices=LOGIN_CHOICES, max_length=50, default=LOGIN_EMAIL
    )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

