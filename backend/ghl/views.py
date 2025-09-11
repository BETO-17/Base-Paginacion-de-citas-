import requests
import json
from django.http import JsonResponse
from django.views import View

# 🔑 Token privado de GHL (puedes moverlo a settings.py como variable)
GHL_API_KEY = "pit-3ff13585-dab4-4acf-b61a-aacfcd8c29fb"
GHL_BASE_URL = "https://rest.gohighlevel.com/v1"
API_VERSION = "2021-07-28"


class CalendarListView(View):
    def get(self, request):
        url = f"{GHL_BASE_URL}/calendars/"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Version": API_VERSION,
        }
        response = requests.get(url, headers=headers)
        return JsonResponse(response.json())


class AppointmentCreateView(View):
    def post(self, request):
        data = json.loads(request.body)

        url = f"{GHL_BASE_URL}/appointments/"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Version": API_VERSION,
            "Content-Type": "application/json",
        }

        payload = {
            "calendarId": data.get("calendarId"),
            "contactId": data.get("contactId"),
            "startTime": data.get("startTime"),  # formato ISO8601
            "endTime": data.get("endTime"),
        }

        response = requests.post(url, headers=headers, json=payload)
        return JsonResponse(response.json())
