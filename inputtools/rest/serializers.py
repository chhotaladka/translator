from rest_framework import serializers
from rest_framework.serializers import CharField

class WordSuggestionSerializer(serializers.Serializer):
    word = CharField(style={'base_template': 'textarea.html'}, required=True)
    suggestions = CharField(style={'base_template': 'textarea.html'}, allow_blank=True, required=False)

