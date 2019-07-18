'''
Created on 19-Jul-2019

@author: anshul
'''

from rest_framework import views
from rest_framework.response import Response

from translator.rest.serializers import TranslatorSerializer

class TranslateView(views.APIView):
    @classmethod
    def get_extra_actions(cls):
        return []
        
    def post(self, request):
        data = request.data.get('data', None)
        
        translation = 'Call translation API'
        
        result = TranslatorSerializer({"text": data, "translation": translation}).data
        return Response(result)
    
class SaveView(views.APIView):
    @classmethod
    def get_extra_actions(cls):
        return []
        
    def post(self, request):
        data = request.data.get('data', None)
        
        translation = 'Call translation API'
        
        result = TranslatorSerializer({"text": data, "translation": translation}).data
        #Save it somewhere
        return Response(result)
        
    def get(self, request):
        #Access protected to authorized people only
        result = TranslatorSerializer({"text": "Fetch from DB", "translation": "TBD"}).data
        return Response(result)


