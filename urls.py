from django.urls import path
from .views import *

urlpatterns = [
    path('', prediction_api),
    #####################################################################
    path('', home),
    path('get-response', get_response),
    path('masters/get-reponse', get_response),
]