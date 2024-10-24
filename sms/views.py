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
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)


def send_sms(request):
    if request.method == "POST":
        # Handle SMS sending logic
        phone = request.POST.get("msisdn")
        message = request.POST.get("message")

        key = settings.KEY
        sender_id = settings.SENDER_ID

        data = {
            "key": key,
            "msisdn": phone,
            "message": message,
            "sender_id": sender_id,
            # "callback_url": callback_url,
            "callback_url":"https://smsapi-production-b762.up.railway.app/callback-url/"
        }
        try:
            response = requests.post(settings.API_URL, data=data)
            api_response = response.json()  # Parse the JSON response
            if response.status_code == 200 and api_response.get("status") == "1701":
                return JsonResponse(api_response)
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
        logging.info(dlr_data)
        channel_layer = get_channel_layer()
        dlr_data = json.loads(dlr_data)
        async_to_sync(channel_layer.group_send)(
            "dlr_updates",
            {
                "type": "dlr_message",
                "message": dlr_data,
            },
        )
        return HttpResponse("DLR received", status=200)
