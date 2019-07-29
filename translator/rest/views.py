'''
Created on 19-Jul-2019

@author: anshul
'''

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from translator.rest.serializers import (TranslatorSerializer,TranslationListing)
from translator.backend import translator

from translator.models import (Wordlist, Translations)
from django.shortcuts import get_object_or_404

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
    http_method_names = ['get', 'head', 'post', 'put']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
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
                return Response({'detail': 'Translation is not provided'}, status=status.HTTP_400_BAD_REQUEST)
            src, created = Translations.objects.get_or_create(source=text, src_lang= 'EN')
            # if(created is False):
            #     print('Updating, if necessary')
            dest, created = Translations.objects.get_or_create(source=translation, src_lang= 'HI')
            # if(created is False):
            #     print('Updating, if necessary')
            #print(src.target.all())
            #print(dest)
            src.target.add(dest)
            dest.target.add(src)
            src.save()
            dest.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        #Access protected to authorized people only
        qs = Translations.objects.all()
        obj = get_object_or_404(qs, pk=pk)
        result = TranslationListing(obj).data
        return Response(result)

    def list(self, request, format=None):
        #Access protected to authorized people only
        qs = Translations.objects.all()
        result = TranslationListing(qs, many=True).data
        return Response(result)


