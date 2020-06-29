from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class CreateReviewForm(forms.ModelForm):

    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "rating",
        )
        widgets = {
            "review": forms.TextInput(
                attrs={"placeholder": _("Please input review at this restaurant")}
            ),
        }

    def save(self):
        review = super().save(commit=False)
        return review
