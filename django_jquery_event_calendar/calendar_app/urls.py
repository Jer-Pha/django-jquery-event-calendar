from django.urls import path

from .views import view_event, view_calendar

urlpatterns = [
    path('', view_calendar, name='view_calendar'),
    path('view-event/<event_id>/', view_event, name='view_event'),
]