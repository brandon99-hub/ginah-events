from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, Ticket, Reminder
from .forms import ReviewForm, TicketBookingForm


# Event List View
@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# Event Detail View
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {
        'event': event,
    })

# Contact Page View
@login_required
def contact(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose the full message
        full_message = f"Message from {name} ({email}):\n\n{message}"

        try:
            send_mail(
                subject,  # Subject of the email
                full_message,  # Message body
                settings.DEFAULT_FROM_EMAIL,  # Sender's email
                [settings.DEFAULT_FROM_EMAIL],  # Recipient list (your email)
                fail_silently=False,  # Raise an error if email sending fails
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred while sending your message: {e}")

        return redirect('contact')  # Redirect back to the contact page after submission
    else:
        return render(request, 'events/contact.html')

# Buy Ticket View
@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.available_tickets > 0:
        Ticket.objects.create(event=event, user=request.user)
        event.available_tickets -= 1
        event.save()
        messages.success(request, 'Ticket purchased successfully!')
    else:
        messages.error(request, 'Sorry, this event is sold out.')

    return redirect('event_detail', event_id=event_id)

def pesapal_charge(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        try:
            # Example: Calculate the amount (assuming event.price is in KES).
            # Pesapal may require the amount in a specific format.
            amount = event.price

            # Here you would add your Pesapal integration logic.
            # For demonstration purposes, we simulate a successful call with a dummy redirect URL.
            pesapal_payment_url = "https://pesapal.com/api/payment?order_id=12345"

            # Return the redirect URL so your front end can send the user there.
            return JsonResponse({'redirect_url': pesapal_payment_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# User Signup View
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'events/signup.html'

# Set Reminder View
@login_required
def set_reminder(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Calculate reminder time (e.g., 24 hours before event start time)
    reminder_time = event.date - timezone.timedelta(days=1)

    Reminder.objects.create(user=request.user, event=event, reminder_time=reminder_time)

    messages.success(request, f'Reminder set for {event.title}.')
    return redirect('event_list')

# Save Review View
@login_required
def save_review(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('event_detail', event_id=event_id)
    else:
        form = ReviewForm()

    return render(request, 'events/event_detail.html', {'form': form, 'event': event})

# Book Tickets View
@login_required
def book_tickets(request):
    if request.method == "POST":
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your ticket has been booked successfully!")
            return redirect('booking_success')  # Redirect to a success page
    else:
        form = TicketBookingForm()

    return render(request, 'events/book_tickets.html', {'form': form})

# Booking Success View
def booking_success(request):
    return render(request, 'events/booking_success.html')


