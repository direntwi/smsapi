from django.urls import path
from . import views

urlpatterns = [
    path('send-sms/', views.send_sms, name='send_sms'),
]
