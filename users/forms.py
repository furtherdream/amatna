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
                self.add_error("password", forms.ValidationError("Password id wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "nickname")

    password = forms.CharField(
        label="패스워드",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해 주세요."}),
    )
    password1 = forms.CharField(
        label="패스워드 확인",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 확인해 주세요."}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password comfirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
