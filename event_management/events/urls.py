from django.shortcuts import redirect
from . import views
from .views import book_tickets,booking_success
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/buy/', views.buy_ticket, name='buy_ticket'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('contact/', views.contact, name='contact'),
    path('event/<int:event_id>/reminder/', views.set_reminder, name='set_reminder'),
    path('event/<int:event_id>/review/', views.save_review, name='save_review'),
    path('book-tickets/', views.book_tickets, name='book_tickets'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('', auth_views.LoginView.as_view( ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('event/<int:event_id>/pesapal_charge/', views.pesapal_charge, name='pesapal_charge'),  # New URL pattern
]
