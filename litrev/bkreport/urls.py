from django.urls import path
from . import views

# uri start with .../rev/

urlpatterns = [
    path('ticket/add/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('review/add/', views.new_review, name='add_review'),
    path('review/add/<int:ticket_id>/', views.new_review_from_ticket, name='add_review_from_ticket'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('ticket/edit/<int:pk>/', views.TicketUpdateView.as_view(), name='edit_ticket'),
    path('review/edit/<int:pk>/', views.ReviewUpdateView.as_view(), name='edit_review')
]
