import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.base import ContentFile
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    # FormView에서는 get이나 post를 쓰지 않는다.
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    messages.info(request, _("Bye bye :) See you soon."))
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def kakao_login(request):
    cilent_id = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={cilent_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException(_("Kakao authenfication is not completed"))
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        properties = profile_json.get("properties")
        email = kakao_account.get("email")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(_("Please log in with another method"))
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                nickname=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = ("nickname",)
    success_message = _("Your profile is edited")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["nickname"].widget.attrs = {
            "label": _("Nickname"),
        }
        return form

    def get_object(self, queryset=None):
        return self.request.user


class UpdatePasswordView(
    PasswordChangeView,
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
):

    template_name = "users/update_password.html"
    success_message = _("Your password is changed")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {
            "placeholder": _("Enter current password"),
        }
        form.fields["new_password1"].widget.attrs = {
            "placeholder": _("Enter new password")
        }
        form.fields["new_password2"].widget.attrs = {
            "placeholder": _("Confirm new password")
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()
