from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
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
        ticket = request.POST.get('ticket')
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