from django.forms import ModelForm, RadioSelect

from bkreport.models import Review, UserFollows


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


class UserFollowsForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
