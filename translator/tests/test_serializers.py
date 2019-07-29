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
    #Retrieving saved lists is not allowed without credentials
    def test_save_translation(self):
      response = self.client.post('/rest/save/', 
                                    {'text': 'Data needs translation.',
                                     'translation': 'deta ko anuvaad ki jaroorat hai'})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='Data needs translation.',
                          count=1,
                          status_code=status.HTTP_200_OK)

    def test_save_without_translation_gives_error(self):
      response = self.client.post('/rest/save/', 
                                    {'text': 'Data needs translation.'})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='Translation is not provided',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_save_without_text_gives_error(self):
      response = self.client.post('/rest/save/', 
                                    {'translation': 'deta ko anuvaad ki jaroorat hai'})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='This field is required.',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_save_empty_text_gives_error(self):
      response = self.client.post('/rest/save/', 
                                    {'text': '',
                                     'translation': 'deta ko anuvaad ki jaroorat hai'})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='This field may not be blank.',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_save_empty_translation_gives_error(self):
      response = self.client.post('/rest/save/', 
                                    {'text': 'Data needs translation.',
                                     'translation': ''})
      response.render()
      #print(response.rendered_content)
      self.assertContains(response, 
                          text='Translation is not provided',
                          count=1,
                          status_code=status.HTTP_400_BAD_REQUEST)

    def test_get_without_login_gives_error(self):
        response = self.client.get('/rest/save/')
        response.render()
        #print(response.rendered_content)
        self.assertContains(response, 
                            text='Authentication credentials were not provided.',
                            count=1,
                            status_code=status.HTTP_403_FORBIDDEN)

    def test_get_with_login_gets_list(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/rest/save/', 
                                    {'text': 'Data needs translation.',
                                     'translation': 'deta ko anuvaad ki jaroorat hai'})
        self.client.post('/rest/save/', 
                                    {'text': 'Data needs more translation.',
                                     'translation': 'deta ko aur anuvaad ki jaroorat hai'})
        response = self.client.get('/rest/save/')
        response.render()
        #print(response.rendered_content)
        listing = response.rendered_content
        #print(listing)
        self.assertContains(response, 
                            text='Data needs more translation.',
                            count=1,
                            status_code=status.HTTP_200_OK)
