from pprint import pprint

from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from bkreport.forms import TicketForm, ReviewForm
from bkreport.models import Ticket, Review


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def new_ticket(request):
    context = {}
    if request.method == "POST":
        description = request.POST.get('description')
        image = request.POST.get('image')
        title = request.POST.get('title')
        user = request.user
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(title=title, description=description, user=user, image=image)
            ticket.save()
            return redirect('new_ticket')
        else:
            context["message"] = "Erreur dans le formulaire"
    form = TicketForm()
    context["form"] = form
    return render(request, 'bkreport/ticket/new.html', context=context)


def new_review(request):
    context = {}
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=request.POST.get('ticket'))
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        user = request.user
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(rating=rating,
                                           headline=headline,
                                           body=body,
                                           user=user,
                                           ticket=ticket)
            review.save()
            return redirect('new_review')
    form = ReviewForm()
    context["form"] = form
    return render(request, 'bkreport/review/new.html', context=context)


class TicketCreateView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ReviewCreateView(CreateView):
    model = Review
    fields = ['ticket', 'rating', 'headline', 'body']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    class Meta:
        widgets = {
            'rating': forms.RadioSelect()
        }

