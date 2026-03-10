from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import time
import os
import threading


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


def _start_cycle(fastapi_host):
    """Background thread function to execute the start cycle"""
    try:
        fastapi_ping_url = f"http://{fastapi_host}:8101/api/ping/"
        fastapi_start_url = f"http://{fastapi_host}:8101/api/start/"

        # Send ping to FastAPI
        requests.post(
            fastapi_ping_url,
            json={"ping": "ping"},
            headers={"Content-Type": "application/json"},
            timeout=15.0
        )

        # Wait 3 seconds
        time.sleep(3)

        # Send boom to FastAPI
        requests.post(
            fastapi_ping_url,
            json={"ping": "boom"},
            headers={"Content-Type": "application/json"},
            timeout=15.0
        )

        # Wait 5 seconds for delay before next cycle
        time.sleep(5)

        # Send start request to FastAPI to continue the cycle (non-blocking)
        requests.post(
            fastapi_start_url,
            json={"start": "start"},
            headers={"Content-Type": "application/json"},
            timeout=15.0
        )
    except Exception as e:
        print(f"Error in start cycle: {e}")


@csrf_exempt
@require_http_methods(["POST"])
def start(request):
    try:
        data = json.loads(request.body)
        if data.get("start") == "start":
            # Get FastAPI host from environment variable (default to localhost for standalone)
            fastapi_host = os.getenv("FASTAPI_HOST", "127.0.0.1")

            # Start the cycle in a background thread so this endpoint returns immediately
            thread = threading.Thread(target=_start_cycle, args=(fastapi_host,), daemon=True)
            thread.start()

            return JsonResponse({"message": "Requests sent successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
