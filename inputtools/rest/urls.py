from django.urls import path, include
from rest_framework import routers
from inputtools.rest import views

router = routers.SimpleRouter()
router.register(r'inputtools', views.WordSuggestionView, base_name='inputtools')

urlpatterns = [
    path(r'', 
         include(router.urls), name="inputtools"),
    ]
