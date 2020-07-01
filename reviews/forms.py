from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ("review",)
        widgets = {
            "review": forms.TextInput(
                attrs={"placeholder": _("Please input review at this restaurant")}
            ),
        }

    def save(self):
        review = super().save(commit=False)
        return review
