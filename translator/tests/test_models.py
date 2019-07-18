'''
Created on 18-Jul-2019

@author: craft
'''
from django.test import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from unittest.case import skip

class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester",
                                           email="tester@testing.co",
                                           password="secret")
        TestCase.setUp(self)
        print("In method", self._testMethodName)

    def tearDown(self):
        TestCase.tearDown(self)


class TestModel(BaseTest):
    pass
            
