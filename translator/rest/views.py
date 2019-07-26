'''
Created on 19-Jul-2019

@author: anshul
'''

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from translator.rest.serializers import TranslatorSerializer
from translator.backend import translator

from translator.models import (Wordlist, Translations)

class TranslateView(viewsets.ViewSet):
    http_method_names = ['post', 'put']
    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, format=None):
        serializer = TranslatorSerializer(data=request.data)
        if serializer.is_valid():
            engine = translator.Engine()
            translation = engine.translate(serializer.data.get('text'))
            result = TranslatorSerializer({"text": serializer.data.get('text'), 
                                         "translation": translation}).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    def create(self, request, format=None):
        serializer = TranslatorSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.data.get('text')
            translation = serializer.data.get('translation', None)
            if translation is None or len(translation.strip()) ==0:
                serializer.errors['translation']='This field must be provided'
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            src = Translations.objects.create(source=text, src_lang= 'EN')
            dest = Translations.objects.create(source=translation, src_lang= 'HI')
            src.target = dest
            dest.target = src
            
            src.save()
            dest.save()
            
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request):
        #Access protected to authorized people only
        result = TranslatorSerializer({"text": "Fetch from DB", "translation": "TBD"}).data
        return Response(result)

    def list(self, request, format=None):
        #Access protected to authorized people only
        result = TranslatorSerializer([{"text": "Fetch from DB", "translation": "TBD"}], many=True).data
        return Response(result)


