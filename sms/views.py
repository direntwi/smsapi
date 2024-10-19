from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import logging
import requests
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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


# @csrf_exempt
# def receive_dlr(request):
#     if request.method == "POST":
#         dlr_data = request.body.decode("utf-8")  # Get DLR data from request
#         logging.info(dlr_data)  # Log the DLR into a separate log file

#         # Respond to acknowledge receipt of the DLR
#         return HttpResponse("DLR received", status=200)


@csrf_exempt
def receive_dlr(request):
    if request.method == "POST":
        dlr_data = request.body.decode("utf-8")  # Get DLR data from request
        logging.info(dlr_data)  # Log the DLR into a separate log file
        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dlr_updates",
            {
                "type": "dlr_message",
                "message": dlr_data,
            },
        )

        # Respond to acknowledge receipt of the DLR
        return HttpResponse("DLR received", status=200)


def dlr_updates(request):
    try:
        with open("logfile.log", "r") as log_file:
            lines = log_file.readlines()
            if lines:
                last_line = lines[-1].strip()  # Get the last line and remove whitespace

                # Check if the line is not empty before trying to parse it
                if last_line:
                    try:
                        latest_dlr = json.loads(last_line)  # Try to parse it as JSON
                        return JsonResponse(latest_dlr)
                    except json.JSONDecodeError:
                        return JsonResponse(
                            {"error": "Invalid JSON format in the log file."},
                            status=500,
                        )
                else:
                    return JsonResponse(
                        {"dlr_status": "No updates yet (empty line)."}, status=204
                    )
            else:
                return JsonResponse({"dlr_status": "Log file is empty."}, status=204)
    except FileNotFoundError:
        return JsonResponse({"error": "Log file not found."}, status=404)
