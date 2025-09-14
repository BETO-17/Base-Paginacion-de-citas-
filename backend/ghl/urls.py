from django.urls import path
from .views import CalendarListView, AppointmentCreateView, AppointmentListView

urlpatterns = [
    path("calendars/", CalendarListView.as_view(), name="ghl_calendars"),
    path("ghl/appointment/", AppointmentCreateView.as_view(), name="ghl_appointment"),
    path("ghl/appointments/", AppointmentListView.as_view(), name="ghl_appointments"),  # 👈 nueva
]

