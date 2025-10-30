from rest_framework import viewsets, permissions
from .models import Habit, HabitEntry
from .serializers import HabitSerializer, HabitEntrySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        habits = self.get_queryset()
        serializer = self.get_serializer(habits, many=True)
        data = serializer.data

        for habit_data in data:
            habit_id = habit_data["id"]
            entries = HabitEntry.objects.filter(habit_id=habit_id).order_by("date")

            streak = 0
            max_streak = 0
            last_date = None

            for entry in entries:
                if last_date:
                    if (entry.date - last_date).days == 1:
                        streak += 1
                    elif (entry.date - last_date).days > 1:
                        streak = 1
                else:
                    streak = 1
                last_date = entry.date
                max_streak = max(max_streak, streak)

            habit_data["entries_count"] = entries.count()
            habit_data["current_streak"] = streak
            habit_data["max_streak"] = max_streak

        return Response(data)


class HabitEntryViewSet(viewsets.ModelViewSet):
    queryset = HabitEntry.objects.all()
    serializer_class = HabitEntrySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return HabitEntry.objects.all()


@api_view(['GET'])
def analytics_view(request):
    data = []
    habits = Habit.objects.all()
    for habit in habits:
        total_entries = HabitEntry.objects.filter(habit=habit).count()
        progress = (total_entries / habit.duration) * 100 if habit.duration else 0
        data.append({
            'name': habit.name,
            'duration': habit.duration,
            'entries': total_entries,
            'progress': round(progress, 2),
        })
    return Response(data)
