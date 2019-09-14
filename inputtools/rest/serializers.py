from rest_framework import serializers
from rest_framework.serializers import CharField, ListField

class WordSuggestionSerializer(serializers.Serializer):
    word = CharField(style={'base_template': 'textarea.html'}, required=True)
    lang = CharField(style={'base_template': 'textarea.html'}, allow_blank=True, required=False, default='hi')
    suggestions = ListField(child=CharField(),min_length =0, allow_empty=True, required=False)

