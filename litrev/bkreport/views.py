from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from bkreport.forms import TicketForm
from bkreport.models import Ticket


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def new_ticket(request):
    context = {}
    if request.method == "POST":
        pprint(request.POST)
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