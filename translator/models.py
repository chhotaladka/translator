"""
@author: Anshul Thakur
"""
from django.db import models

LANGUAGES = [('EN', 'English'),
             ('HI', 'Hindi')]
    
class Wordlist(models.Model):
    source = models.TextField(blank=False, null=False)
    src_lang = models.CharField(options = LANGUAGES, blank=False, default='EN')
    
    target = models.ForeignKey("Translations", null=False)


class Translations(models.Model):
    source = models.TextField(blank=False, null=False)
    src_lang = models.CharField(options = LANGUAGES, blank=False, default='EN')
    
    target = models.ForeignKey("Translations", null=False)