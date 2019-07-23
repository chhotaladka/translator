'''
Created on 19-Jul-2019

@author: anshul
'''

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from translator.rest.serializers import TranslatorSerializer
from translator.backend import translator

class TranslateView(viewsets.ViewSet):
    http_method_names = ['post', 'put']
    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request, format=None):
        data = request.data.get('text', None)
        
        engine = translator.Engine(engine='dummy')
        translation = engine.translate(data)
        
        result = TranslatorSerializer({"text": data, "translation": translation}).data
        return Response(result)

    def create(self, request, format=None):
        data = request.data.get('text', None)
        
        engine = translator.Engine()
        translation = engine.translate(data)

        result = TranslatorSerializer({"text": data, "translation": translation}).data
        return Response(result)
    
class SaveView(viewsets.ViewSet):
    http_method_names = ['get', 'head']
    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request):
        data = request.data.get('text', None)
        translation = request.data.get('translation', None)
        
        result = TranslatorSerializer({"text": data, "translation": translation}).data
        #Save it somewhere
        return Response(result)
        
    def retrieve(self, request):
        #Access protected to authorized people only
        result = TranslatorSerializer({"text": "Fetch from DB", "translation": "TBD"}).data
        return Response(result)

    def list(self, request, format=None):
        #Access protected to authorized people only
        result = TranslatorSerializer([{"text": "Fetch from DB", "translation": "TBD"}], many=True).data
        return Response(result)


