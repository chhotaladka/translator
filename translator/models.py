"""
@author: Anshul Thakur
"""
from django.db import models

LANGUAGES = [('EN', 'English'),
             ('HI', 'Hindi')]
    
class Wordlist(models.Model):
    source = models.TextField(blank=False, null=False)
    src_lang = models.CharField(choices = LANGUAGES, 
                                blank=False, 
                                default='EN',
                                max_length=2)
    
    target = models.ForeignKey("Translations", 
                               null=False, 
                               on_delete=models.DO_NOTHING)


class Translations(models.Model):
    source = models.TextField(blank=False, null=False)
    src_lang = models.CharField(choices = LANGUAGES, 
                                blank=False, 
                                default='EN',
                                max_length=2)
    
    target = models.ForeignKey("Translations", 
                               null=False,
                               on_delete=models.DO_NOTHING)