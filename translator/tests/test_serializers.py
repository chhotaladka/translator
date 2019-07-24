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
        #print("In method", self._testMethodName)

    def tearDown(self):
        APITestCase.tearDown(self)

class translateAPITests(BaseTest):
    def test_translate_non_empty_string(self):
      response = self.client.post('/rest/translate/', 
                                    {'text': 'Data needs translation.',})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='Data needs translation.',
                          count=1,
                          status_code=status.HTTP_200_OK)

    def test_invalid_request_gives_error(self):
      response = self.client.post('/rest/translate/', 
                                  {})
      response.render()
      self.assertContains(response, 
                          text='This field is required.',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_empty_string_gives_error(self):
      response = self.client.post('/rest/translate/', 
                                  {'text': ''})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='This field may not be blank.',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_blank_string_gives_error(self):
      response = self.client.post('/rest/translate/', 
                                  {'text': '   '})
      response.render()
      self.assertContains(response, 
                          text='This field may not be blank.',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)
class saveAPITests(BaseTest):
    #Nothing is allowed without login credentials
    pass
