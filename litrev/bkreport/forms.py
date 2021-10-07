from django.forms import ModelForm, RadioSelect

from bkreport.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["ticket", "rating", "headline", "body"]
        widgets = {"rating": RadioSelect()}


class ReviewFormFromTicket(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
        widgets = {"rating": RadioSelect()}
