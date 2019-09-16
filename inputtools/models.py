from django.db import models

# Create your models here.


LANGUAGES = [('EN', 'English'),
             ('HI', 'Hindi')]
    
class Wordlist(models.Model):
    word = models.TextField(blank=False, 
                              null=False, 
                              db_index=True, 
                              unique=True,  max_length=255)
    lang = models.CharField(choices = LANGUAGES, 
                                default='EN',
                                max_length=2)

    def __str__(self):
    	return self.word;


class BulkCreateManager(object):

    model = None
    chunk_size = None
    instances = None

    def __init__(self, model, chunk_size=1000, *args):
        self.model = model
        self.chunk_size = chunk_size
        self.instances = []

    def append(self, instance):
        if self.chunk_size and len(self.instances) > self.chunk_size:
            self.create()
            self.instances = []

        self.instances.append(instance)

    def create(self):
        print("Bulk create {s} : objs {l}".format(s=self.model, l=len(self.instances)));
        self.model.objects.bulk_create(self.instances,  ignore_conflicts=True)