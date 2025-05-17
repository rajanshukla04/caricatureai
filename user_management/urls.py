from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('qr-checkin/', views.qr_checkin, name='qr_checkin'),   
    path('manual-checkin/', views.manual_checkin, name='manual_checkin'),
    path('success/<int:user_id>/', views.success_page, name='success_page'),
]