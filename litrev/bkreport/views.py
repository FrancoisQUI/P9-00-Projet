from pprint import pprint

from django import forms
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from bkreport.models import Ticket, Review


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class TicketDetailView(DetailView):
    model = Ticket


class TicketCreateView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ReviewDetailView(DetailView):
    model = Review


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


class ReviewCreateFromTicketView(CreateView):
    model = Review
    fields = ['rating', 'headline', 'body']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.ticket = self.kwargs["pk"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateFromTicketView, self).get_context_data(**kwargs)
        try:
            context["ticket"] = self.kwargs["pk"]
        except KeyError:
            print("No ticket")
        return context

    class Meta:
        widgets = {
            'rating': forms.RadioSelect()
        }


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['rating', 'headline', 'body']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    class Meta:
        widgets = {
            'rating': forms.RadioSelect()
        }