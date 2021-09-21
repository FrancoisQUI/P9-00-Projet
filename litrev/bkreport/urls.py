from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='book-index'),
    path('ticket/add/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('review/add/', views.ReviewCreateView.as_view(), name='add_review'),
    # path('review/detail/', , name='review_detail')
]