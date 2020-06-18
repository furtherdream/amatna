from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="이메일", widget=forms.EmailInput(attrs={"placeholder": "이메일을 입력해 주세요."})
    )
    password = forms.CharField(
        label="패스워드",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해 주세요."}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        print("clean_password")

