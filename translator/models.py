"""
@author: Anshul Thakur
"""
from django.db import models

LANGUAGES = [('EN', 'English'),
             ('HI', 'Hindi')]
    
class Wordlist(models.Model):
    source = models.TextField(blank=False, 
                              null=False, 
                              db_index=True, 
                              unique=True)
    src_lang = models.CharField(choices = LANGUAGES, 
                                default='EN',
                                max_length=2)
    
    target = models.ManyToManyField("self")


class Translations(models.Model):
    source = models.TextField(blank=False, 
                              null=False, 
                              db_index=True, 
                              unique=True)
    src_lang = models.CharField(choices = LANGUAGES, 
                                blank=False, 
                                default='EN',
                                max_length=2)
    
    target = models.ManyToManyField("self")
