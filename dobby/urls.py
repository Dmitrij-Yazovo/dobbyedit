from django.urls import path
from . import views

app_name = 'dobby'

urlpatterns = [
    path('edit/', views.edit, name='edit'),    
    # path('result/', views.result, name='result'),     
    path('loading/', views.loading, name='loading'), 
    path('result/', views.result, name='result'),    
]