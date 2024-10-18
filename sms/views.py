from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

logger = logging.getLogger('dlr_logger')
handler = logging.FileHandler('dlr_log_file.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



# @csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        # Handle SMS sending logic
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        data = {
            "key" : settings.KEY,
            "msisdn" : phone,
            "message" :  message,
            "sender_id" : settings.SENDER_ID,
        }

        try:
            response = requests.post(settings.API_URL, data=data)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'success': False, 'message': 'Failed to send message.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return render(request, 'sms/send_sms.html')

def send_sms1(request):
    if request.method == 'POST':
        # Handle SMS sending logic
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        data = {
            "key" : settings.KEY,
            "msisdn" : phone,
            "message" :  message,
            "sender_id" : settings.SENDER_ID,
            "callback_url": settings.CALLBACK_URL
        }

        try:
            response = requests.post(settings.API_URL, data=data)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'success': False, 'message': 'Failed to send message.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return render(request, 'sms/sms_1.html')


@csrf_exempt
def receive_dlr(request):
    if request.method == 'POST':
        dlr_data = request.body.decode('utf-8')  # Get DLR data from request
        logger.info(dlr_data)  # Log the DLR into a separate log file

        # Respond to acknowledge receipt of the DLR
        return HttpResponse('DLR received', status=200)