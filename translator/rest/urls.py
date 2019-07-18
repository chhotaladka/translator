'''
Created on 18-Jul-2019

@author: anshul
'''
from django.urls import path, include
from rest_framework import routers
from translator.rest import views

router = routers.SimpleRouter()
router.register(r'translate', views.TranslateView, base_name='translate')
router.register(r'save', views.SaveView, base_name='save')

urlpatterns = [
    path(r'', 
         include(router.urls), name="translator"),
    ]
