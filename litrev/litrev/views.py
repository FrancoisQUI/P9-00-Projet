from itertools import chain
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import CharField, Value
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_list_or_404

from .forms import SignUpForm
from bkreport.models import UserFollows, Review, Ticket


def index(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is None:
            context = {
                "error": "Invalid password or username",
                "form": form}
            return render(request, "litrev/index.html", context)
        login(request, user)
    return render(request, "litrev/index.html", context={"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to flux page
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'litrev/signup.html', {'form': form})


def disconnect(request):
    logout(request)
    return redirect("site-index")


def feed(request):
    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'litrev/feed.html', context={'posts': posts})


def subs(request):
    user_pk = request.user.id
    follows = UserFollows.objects.get(user_id=user_pk)
    followers = UserFollows.objects.get(followed_user_id=user_pk)
    context = {
        "follows": follows,
        "followers": followers,
    }
    return render(request, 'litrev/subs.html', context)


def post(request):
    return HttpResponse("Post page")
