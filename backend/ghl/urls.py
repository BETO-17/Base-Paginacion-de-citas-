from django.urls import path
from .views import (
    CalendarListView,
    AppointmentCreateView,
    AppointmentDetailView,
    BatchAppointmentsView,
   appointment_list,
   AllGHLAppointmentsView

)

urlpatterns = [
    path("calendars/", CalendarListView.as_view(), name="ghl_calendars"),
    path("ghl/appointment/", AppointmentCreateView.as_view(), name="ghl_appointment"),
    path("ghl/appointments/<str:event_id>/", AppointmentDetailView.as_view(), name="ghl_appointment_detail"),
    path("ghl/appointments/batch/", BatchAppointmentsView.as_view(), name="batch_appointments"),
    path('api/appointments/', appointment_list, name='appointment_list'),
    path('api/ghl-appointments/', AllGHLAppointmentsView.as_view(), name='all_ghl_appointments')

]
