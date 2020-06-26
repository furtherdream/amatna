from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"placeholder": _("Please enter your email.")}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Please enter your password.")}
        ),
    )

    def clean(self):
        # 클린을 사용하면 그 필드에 직접 에러를 추가해주면 됨.
        # clean_password(), clean_username() 이렇데 할거면 그냥 error를 raise한면 됨
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
                # clean()을 썼다면 무조건 cleaned_data를 리턴해줘야 함
            else:
                self.add_error(
                    "password", forms.ValidationError(_("Password id wrong"))
                )
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError(_("User does not exist")))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "nickname")
        widgets = {
            "email": forms.TextInput(
                attrs={"placeholder": _("Please enter your email.")}
            ),
            "nickname": forms.TextInput(
                attrs={"placeholder": _("Please enter your nickname.")}
            ),
        }

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Please enter your password.")}
        ),
    )
    password1 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Please confirm your password.")}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(_("User already exists with that email"))
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError(_("Password comfirmation does not match"))
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
