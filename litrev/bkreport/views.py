from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from bkreport.forms import TicketForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def new_ticket(request):
    form = TicketForm()
    context = {
        "form" : form
    }
    return render(request, 'bkreport/ticket/new.html', context=context)