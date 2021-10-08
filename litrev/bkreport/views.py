from pprint import pprint

from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from bkreport.models import Ticket, Review
from bkreport.forms import ReviewForm, ReviewFormFromTicket


def new_review(request):
    if request.method == "POST":
        ticket_id = request.POST.get('ticket')
        ticket = Ticket.objects.get(pk=ticket_id)
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        user = request.user
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(ticket=ticket,
                                           rating=rating,
                                           headline=headline,
                                           body=body,
                                           user=user)
            review.save()
            return redirect('feed')

    form = ReviewForm()

    return render(request=request,
                  template_name='bkreport/review/new.html',
                  context={'form': form})


def new_review_from_ticket(request, ticket_id):
    context = {}
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == "POST":
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        user = request.user
        form = ReviewFormFromTicket(request.POST)
        if form.is_valid():
            review = Review.objects.create(ticket=ticket,
                                           rating=rating,
                                           headline=headline,
                                           body=body,
                                           user=user)
            review.save()
            return redirect('feed')

    form = ReviewFormFromTicket()
    context['form'] = form
    context['ticket'] = ticket
    context['show_ticket_only'] = True

    return render(request=request,
                  template_name='bkreport/review/new.html',
                  context=context)


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
            'rating': forms.RadioSelect(),
        }


class ReviewCreateFromTicketView(CreateView):
    model = Review
    fields = ['rating', 'headline', 'body']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateFromTicketView, self).get_context_data(**kwargs)
        try:
            context["ticket_id"] = self.kwargs["ticket_id"]
        except KeyError:
            print("No ticket")
        return context

    class Meta:
        widget = {
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


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('post')


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy('post')
