from itertools import chain
from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import CharField, Value
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .forms import SignUpForm
from bkreport.forms import UserFollowsForm
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


def post(request):
    user = request.user

    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'litrev/feed.html', context={'posts': posts, 'delete_button': True})


def subs(request):
    context = {}
    if request.method == 'POST':
        followed_user_pk = request.POST.get('followed_user')
        followed_user = User.objects.get(pk=followed_user_pk)
        user = request.user
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            try:
                follow = UserFollows.objects.create(user=user, followed_user=followed_user)
                follow.save()
                return redirect('subs')
            except IntegrityError:
                context['error_message'] = f'Vous suivez déjà cette personne : {followed_user}'

    user_pk = request.user.id
    follows = UserFollows.objects.filter(user_id=user_pk)
    followers = UserFollows.objects.filter(followed_user_id=user_pk)
    form = UserFollowsForm()
    context["follows"] = follows
    context["followers"] = followers
    context["form"] = form

    pprint(context)
    return render(request, 'litrev/subs.html', context)


class UserFollowsDeleteView(DeleteView):
    model = UserFollows
    success_url = reverse_lazy('subs')
