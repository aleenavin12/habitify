from django.core.mail import send_mail
from django.conf import settings
from .models import Entry  # make sure Entry is imported
from datetime import date

def send_habit_reminders():
    today = date.today()
    pending_entries = Entry.objects.filter(date=today, duration__isnull=True)
    
    for entry in pending_entries:
        send_mail(
            subject=f"Reminder: Complete your habit {entry.habit.name}",
            message=f"Hi {entry.user.username}! You have not completed your habit '{entry.habit.name}' today ({entry.date}). Don't forget to complete it!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[entry.user.email],  # Make sure user has email
        )

