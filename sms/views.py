from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import logging
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

logging.basicConfig(
    level=logging.INFO,
    filename="logfile.log",
    format="%(message)s",
    filemode="a",
)


def send_sms(request):
    if request.method == "POST":
        # Handle SMS sending logic
        phone = request.POST.get("msisdn")
        message = request.POST.get("message")

        data = {
            "key": settings.KEY,
            "msisdn": phone,
            "message": message,
            "sender_id": settings.SENDER_ID,
            "callback_url": settings.CALLBACK_URL,
        }

        try:
            response = requests.post(settings.API_URL, data=data)
            api_response = response.json()
            if response.status_code == 200 and api_response.get("status") == "1701":
                print(JsonResponse(response.json()))
                return JsonResponse(response.json())
            else:
                return JsonResponse(
                    {"success": False, "message": "Failed to send message."}
                )
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return render(request, "sms/sms_1.html")


@csrf_exempt
def receive_dlr(request):
    if request.method == "POST":
        dlr_data = request.body.decode("utf-8")  # Get DLR data from request
        logging.info(dlr_data)  # Log the DLR into a separate log file

        # Respond to acknowledge receipt of the DLR
        return HttpResponse("DLR received", status=200)


def dlr_updates(request):
    # Read the last few lines from the log file for updates (or use any other method)
    try:
        with open("logfile.log", "r") as log_file:
            lines = log_file.readlines()
            if lines:
                latest_dlr = json.loads(lines[-1].strip())  # Get the most recent DLR
                return JsonResponse(latest_dlr)
    except FileNotFoundError:
        return JsonResponse({"dlr_status": "No updates yet"})

    return JsonResponse({"dlr_status": "No updates"})
