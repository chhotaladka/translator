from rest_framework import serializers
from rest_framework.serializers import CharField

class WordSuggestionSerializer(serializers.Serializer):
    word = CharField(style={'base_template': 'textarea.html'}, required=True)
    lang = CharField(style={'base_template': 'textarea.html'}, allow_blank=True, required=False, default='hi')
    suggestions = CharField(style={'base_template': 'textarea.html'}, allow_blank=True, required=False)

