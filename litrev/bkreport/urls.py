from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='book-index'),
    path('ticket/add/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('review/add/', views.ReviewCreateView.as_view(), name='add_review'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name='review_detail'),
    # path('review/detail/', , name='review_detail')
]