from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # se aumento#############
from django.utils.decorators import method_decorator # se aumento#####33
import requests
import json
import logging
from .models import Appointment



# 🔹 Configuración desde settings.py
GHL_API_KEY = settings.GHL_API_KEY
LOCATION_ID = settings.GHL_LOCATION_ID
GHL_BASE_URL = "https://services.leadconnectorhq.com"

logger = logging.getLogger(__name__)

class CalendarListView(View):
    def get(self, request):
        url = f"{GHL_BASE_URL}/calendars/"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }
        params = {"locationId": LOCATION_ID}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return JsonResponse(data, safe=False)
            
        except requests.exceptions.RequestException as e:
            logger.error("Error al obtener calendarios: %s", str(e))
            return JsonResponse({
                "error": "Error de conexión",
                "details": str(e)
            }, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        # Validar campos requeridos
        required_fields = ['calendarId', 'contactId', 'startTime', 'endTime']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)

        payload = {
            "calendarId": data["calendarId"],
            "contactId": data["contactId"],
            "locationId": data.get('locationId', LOCATION_ID),
            "startTime": data["startTime"],
            "endTime": data["endTime"],
            "assignedUserId": data.get("assignedUserId"),
            "ignoreFreeSlotValidation": True,
            "toNotify": data.get("toNotify", []),
        }

        url = f"{GHL_BASE_URL}/calendars/events/appointments"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Version": "2021-07-28",
        }

        try:
            # Enviar a GHL
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            ghl_data = response.json()

            # Guardar en SQLite
            appointment = Appointment.objects.create(
                ghl_id = ghl_data.get("id"),
                calendar_id = data["calendarId"],
                contact_id = data["contactId"],
                title = data.get("title"),
                start_time = data["startTime"],
                end_time = data["endTime"]
            )

            return JsonResponse({
                "message": "Cita creada correctamente",
                "ghl_response": ghl_data,
                "local_id": appointment.id
            }, status=201)

        except requests.exceptions.RequestException as e:
            logger.error("Error al crear cita en GHL: %s", str(e))
            return JsonResponse({"error": "No se pudo crear cita", "details": str(e)}, status=500)


            
@method_decorator(csrf_exempt, name='dispatch')
            
class AppointmentDetailView(View):
    def get(self, request, event_id):
        url = f"{GHL_BASE_URL}/calendars/events/appointments/{event_id}"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return JsonResponse(data, safe=False)
        except requests.exceptions.RequestException as e:
            logger.error("Error al obtener cita: %s", str(e))
            return JsonResponse({
                "error": "Error de conexión",
                "details": str(e)
            }, status=500)
 
@method_decorator(csrf_exempt, name='dispatch')
class BatchAppointmentsView(View):
    def get(self, request):
        appointments = Appointment.objects.all().order_by('-created_at')
        data = [
            {
                "id": a.id,
                "ghl_id": a.ghl_id,
                "calendar_id": a.calendar_id,
                "contact_id": a.contact_id,
                "title": a.title,
                "start_time": a.start_time,
                "end_time": a.end_time,
                "created_at": a.created_at,
            }
            for a in appointments
        ]
        return JsonResponse(data, safe=False)

def appointment_list(request):
    appointments = Appointment.objects.all().values(
        'ghl_id', 'calendar_id', 'contact_id', 'title', 'start_time', 'end_time', 'created_at'
    )
    # Convertir QuerySet a lista
    data = list(appointments)
    return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AllGHLAppointmentsView(View):
    def get(self, request):
        # Traer todos los ghl_id de tu DB local
        appointments = Appointment.objects.all()
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }

        all_data = []

        for a in appointments:
            url = f"{GHL_BASE_URL}/calendars/events/appointments/{a.ghl_id}"
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                resp.raise_for_status()
                all_data.append(resp.json())
            except requests.exceptions.RequestException as e:
                logger.error(f"Error al obtener cita {a.ghl_id}: {str(e)}")
                all_data.append({"ghl_id": a.ghl_id, "error": str(e)})

        return JsonResponse(all_data, safe=False)