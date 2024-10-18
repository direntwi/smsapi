from django.urls import path
from . import views

urlpatterns = [
    path('send-sms/', views.send_sms, name='send_sms'),
    path('callback-url/', views.receive_dlr, name='receive_dlr')
]
