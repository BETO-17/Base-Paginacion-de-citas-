from django.urls import path
from .views import CalendarListView, AppointmentCreateView

urlpatterns = [
    path("calendars/", CalendarListView.as_view(), name="ghl_calendars"),
    path("appointments/create/", AppointmentCreateView.as_view(), name="ghl_create_appointment"),
]
