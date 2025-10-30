from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"


