from django.db import models

# Create your models here.


LANGUAGES = [('EN', 'English'),
             ('HI', 'Hindi')]
    
class Wordlist(models.Model):
    word = models.TextField(blank=False, 
                              null=False, 
                              db_index=True, 
                              unique=True)
    lang = models.CharField(choices = LANGUAGES, 
                                default='EN',
                                max_length=2)

    def __str__(self):
    	return self.word;
    
    