from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from inputtools.rest.serializers import WordSuggestionSerializer

from inputtools.backend import suggestions as suggest

from inputtools.settings import suggestion_settings

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
# # import inputtools.backend.default.libindic
# from inputtools.backend.default.libindic.transliteration import getInstance

# from cmudict import CMUDict

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
                word = transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI);

            suggestions = engine.suggest(word)
            # print(f'word {list(word)} sl {ord(list(word)[-2])}  last word {ord(list(word)[-1])} and suggestions {suggestions}')

            if ord(list(word)[-1]) == 2381:
                if len(suggestions) > 1:
                    print("inserting word without halant")
                    suggestions.insert(0,word[:-1])
                else:
                    print("searching word without halant before ", len(suggestions))
                    suggestions.extend(engine.suggest(word[:-1]))
                    print("searching word without halant before ", len(suggestions))
            if 'en' == lang:
                suggestions.insert(0,word);

            result = WordSuggestionSerializer({"word": serializer.data.get('word'), 
                                         "suggestions": suggestions,"lang":lang}).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
