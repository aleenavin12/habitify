from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitEntryViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet)
router.register(r'entries', HabitEntryViewSet)

urlpatterns = router.urls