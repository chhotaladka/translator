'''
Created on 18-Jul-2019

@author: anshul
'''


from rest_framework import serializers
from rest_framework.serializers import CharField

from translator.models import Translations
class TranslatorSerializer(serializers.Serializer):
    translation = CharField(style={'base_template': 'textarea.html'}, required=False)
    text = CharField(style={'base_template': 'textarea.html'}, required=True)

class TranslationListing(serializers.ModelSerializer):
  class Meta:
    model=Translations
    fields=['id', 'source', 'src_lang', 'target']
