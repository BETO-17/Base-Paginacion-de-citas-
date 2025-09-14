from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # se aumento#############
from django.utils.decorators import method_decorator # se aumento#####33
import requests
import json
import logging


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
                "assignedUserId": data["assignedUserId"],   # 🔹 agregado
                "ignoreFreeSlotValidation": True,
                "toNotify": data.get("toNotify", []),
            }

        url = f"{GHL_BASE_URL}/calendars/events/appointments"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Version": "2021-04-15",
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return JsonResponse(response.json())
            
        except requests.exceptions.HTTPError as e:
            logger.error("Error HTTP al crear cita: %s", response.text)
            return JsonResponse({
                "error": "Error en API externa",
                "status_code": response.status_code,
                "details": response.text
            }, status=response.status_code)
            
        except requests.exceptions.RequestException as e:
            logger.error("Error de conexión al crear cita: %s", str(e))
            return JsonResponse({
                "error": "Error de conexión",
                "details": str(e)
            }, status=500)
class AppointmentListView(View):
    def get(self, request):
        url = f"{GHL_BASE_URL}/calendars/events/appointments"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }
        params = {
            "locationId": LOCATION_ID,
            "limit": 1000  # puedes poner el número que necesites
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return JsonResponse(data, safe=False)

        except requests.exceptions.RequestException as e:
            logger.error("Error al obtener citas: %s", str(e))
            return JsonResponse({
                "error": "Error de conexión",
                "details": str(e)
            }, status=500)
class AppointmentListView(View):
    def get(self, request):
        calendar_id = request.GET.get("calendarId")
        if not calendar_id:
            return JsonResponse({"error": "Debes proporcionar calendarId como parámetro (?calendarId=XXX)"}, status=400)

        url = f"{GHL_BASE_URL}/calendars/events/appointments"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }
        params = {
            "calendarId": calendar_id,
            "limit": 1000
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return JsonResponse(data, safe=False)
        except requests.exceptions.RequestException as e:
            logger.error("Error al obtener citas: %s", str(e))
            return JsonResponse({
                "error": "Error de conexión",
                "details": str(e)
            }, status=500)
