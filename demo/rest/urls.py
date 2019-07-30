'''
Created on 18-Jul-2019

@author: anshul
'''

from django.urls import path, include
from rest_framework import routers
from . import views
from translator.rest.urls import router as translator_router
from inputtools.rest.urls import router as inputtools_router

router = routers.DefaultRouter()
router.register(r'users/current', views.CurrentUserView, base_name='user/current')
router.register(r'users', views.UsersView, base_name='user')

#Extend router with other App specific routers
router.registry.extend(translator_router.registry)
router.registry.extend(inputtools_router.registry)


urlpatterns = [
    path('', include(router.urls), name="demo"),
    path('api-auth/', include('rest_framework.urls'), name="rest_framework"),
    ]
