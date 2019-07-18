'''
Created on 18-Jul-2019

@author: anshul
'''


from rest_framework import serializers
from rest_framework.serializers import CharField

class TranslatorSerializer(serializers.Serializer):
    translation = CharField(style={'base_template': 'textarea.html'}, required=False)
    text = CharField(style={'base_template': 'textarea.html'}, required=True)

