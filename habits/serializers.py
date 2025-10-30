from rest_framework import serializers
from .models import Habit, HabitEntry

class HabitSerializer(serializers.ModelSerializer):
    entries_count = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'name', 'duration', 'entries_count']

    def get_entries_count(self, obj):
        return HabitEntry.objects.filter(habit=obj).count()


class HabitEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEntry
        fields = ['id', 'habit', 'date']
