from django.urls import path
from . import views

urlpatterns = [
    # path('drop', views.home, name='home'),
    path('camera/', views.camera_view, name='camera_view'),    
    path('styles/', views.style_selection, name='style_selection'),
     path('generate/', views.generate_caricature, name='generate_caricature'),
]
