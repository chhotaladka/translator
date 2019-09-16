from django.apps import AppConfig
import nltk

class TranslatorConfig(AppConfig):
    name = 'translator'
    def ready(self):
        nltk.download('punkt')
