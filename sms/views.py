from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import requests
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.

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