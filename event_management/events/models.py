from django.db import models
from django.contrib.auth.models import User

class EventType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Kenyan Shillings (KES)")
    available_tickets = models.IntegerField(default=0)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='event_photos/', blank=True, null=True)  # New field for event photos

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tickets(models.Model):
    EVENT_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('networking', 'Networking Event'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    number_of_tickets = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_type}"