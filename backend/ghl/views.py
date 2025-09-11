from django.conf import settings
from django.views import View
from django.http import JsonResponse
import requests
import json

# 🔹 Configuración desde settings.py
GHL_API_KEY = settings.GHL_API_KEY
LOCATION_ID = settings.GHL_LOCATION_ID
GHL_BASE_URL = "https://services.leadconnectorhq.com"

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
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            return JsonResponse({
                "error": "HTTPError",
                "status_code": response.status_code,
                "content": response.text
            }, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(data, safe=False)


class AppointmentCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        url = f"{GHL_BASE_URL}/appointments"
        headers = {
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Version": "2021-04-15",
        }

        payload = {
            "calendarId": data.get("calendarId"),
            "contactId": data.get("contactId"),
            "startTime": data.get("startTime"),
            "endTime": data.get("endTime"),
            "locationId": LOCATION_ID
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.HTTPError as e:
            return JsonResponse({
                "error": "HTTPError",
                "status_code": response.status_code,
                "content": response.text
            }, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(result)
