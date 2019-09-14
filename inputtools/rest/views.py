from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from inputtools.rest.serializers import WordSuggestionSerializer

from inputtools.backend import suggestions as suggest

from inputtools.settings import suggestion_settings

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


class WordSuggestionView(viewsets.ViewSet):
    http_method_names = ['post', 'put']
    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, format=None):
        serializer = WordSuggestionSerializer(data=request.data)
        if serializer.is_valid():
            engine = suggest.Engine(engine=suggestion_settings.BACKEND)
            word = serializer.data.get('word')
            lang = serializer.data.get('lang')
            if 'en' == lang:
                word = transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)
            suggestions = engine.suggest(word)
            if 'en' == lang:
                suggestions.insert(0,word);
            result = WordSuggestionSerializer({"word": serializer.data.get('word'), 
                                         "suggestions": suggestions,"lang":lang}).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
