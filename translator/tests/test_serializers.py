'''
Created on 18-Jul-2019

@author: anshul
'''
from django.contrib.auth.models import User
from rest_framework.test import (APIRequestFactory, 
                                 force_authenticate, 
                                 APITestCase)

from translator.rest.serializers import TranslatorSerializer
from translator.rest.views import TranslateView, SaveView

from rest_framework.request import Request
from rest_framework import status
from unittest import skip

class BaseTest(APITestCase):
    def setUp(self):
        APITestCase.setUp(self)
        self.user = User.objects.create_superuser(username="Tester", 
                                             email="tester@testing.com", 
                                             password="testing123",
                                             )
        self.password = 'testing123'
        self.factory = APIRequestFactory()
        print("In method", self._testMethodName)

    def tearDown(self):
        APITestCase.tearDown(self)

class translateAPITests(BaseTest):
    pass
                

class saveAPITests(BaseTest):
    #Nothing is allowed without login credentials
    pass
