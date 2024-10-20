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

        data = {
            "key": "niv)woxhjpandc#s93icje1xej6d(j#k1(4ag#g0j0zshl04f61xheuzjlvoaxv)",
            "msisdn": phone,
            "message": message,
            "sender_id": "Test",
            "callback_url": "https://smsapi-production-b762.up.railway.app/callback-url/",
        }
        try:
            response = requests.post(settings.API_URL, data=data)
            if response.status_code == 200:
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
        print(dlr_data)
        logging.info(dlr_data)  # Log the DLR into a separate log file
        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        dlr_data = json.loads(dlr_data)
        async_to_sync(channel_layer.group_send)(
            "dlr_updates",
            {
                "type": "dlr_message",
                "message": dlr_data,
            },
        )

        # Respond to acknowledge receipt of the DLR
        return HttpResponse("DLR received", status=200)
