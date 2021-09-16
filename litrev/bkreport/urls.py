from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='book-index'),
    path('ticket/new/', views.new_ticket, name='new_ticket',)
]