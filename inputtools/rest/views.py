from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from inputtools.rest.serializers import WordSuggestionSerializer


class WordSuggestionView(viewsets.ViewSet):
    http_method_names = ['post', 'put']
    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, format=None):
        serializer = WordSuggestionSerializer(data=request.data)
        if serializer.is_valid():
            word = serializer.data.get('word')
            suggestions = "suggestion 123" # Prepare suggestion list for the `word`
            result = WordSuggestionSerializer({"word": word, 
                                         "suggestions": suggestions}).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
