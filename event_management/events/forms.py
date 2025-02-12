from django import forms
from .models import Review,Tickets

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Write your review'}),
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5', 'placeholder': 'Rating (1-5)'}),
        }

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ['name', 'email', 'phone', 'event_type', 'number_of_tickets']
