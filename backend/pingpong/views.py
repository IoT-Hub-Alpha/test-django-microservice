from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import time


@csrf_exempt
@require_http_methods(["POST"])
def ping(request):
    try:
        data = json.loads(request.body)
        if data.get("ping") == "ping":
            return JsonResponse({"message": "pong"}, status=200)
        elif data.get("ping") == "boom":
            return JsonResponse({"message": 'i don\'t like "BOOM"'}, status=400)
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def start(request):
    try:
        data = json.loads(request.body)
        if data.get("start") == "start":
            # Send ping to 8101
            requests.post(
                "http://127.0.0.1:8101/api/ping/",
                json={"ping": "ping"},
                headers={"Content-Type": "application/json"}
            )

            # Wait 3 seconds
            time.sleep(3)

            # Send boom to 8101
            requests.post(
                "http://127.0.0.1:8101/api/ping/",
                json={"ping": "boom"},
                headers={"Content-Type": "application/json"}
            )

            return JsonResponse({"message": "Requests sent successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
