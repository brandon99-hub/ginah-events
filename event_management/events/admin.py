from django.contrib import admin
from django.contrib import admin
from .models import Event, Ticket, EventType

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(EventType)

# Register your models here.
