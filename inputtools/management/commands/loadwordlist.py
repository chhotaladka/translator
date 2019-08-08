from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError

from inputtools.models import Wordlist
import os

LANGUAGE = ['hi','en']

class Command(BaseCommand):
    help = 'Load word lists in database from file'
    
    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('lang', help='language of the words to be loaded', choices=LANGUAGE)
        parser.add_argument('filename',type=str, help='Name of file containing the words for particular lanuage')
        
    def handle(self, *args, **options):
        # Access arguments inside **options dictionary
        #options={'store_id': '1', 'settings': None, 'pythonpath': None, 
        #         'verbosity': 1, 'traceback': False, 'no_color': False, 'delete': False}
        language = options["lang"]
        filename = options["filename"]
        word_count = 0;
        if os.path.exists(filename):
            with open(filename, encoding="utf8") as file1:
                for line in file1:
                    words = line.split();
                    for w in words:
                        try:
                            Wordlist.objects.create(word=w,lang=language);
                            word_count = word_count + 1;
                        except IntegrityError as e:
                            print(e);
                            print("words loaded ", word_count);
                            continue;

                print("total words loaded ", word_count);
        else:
            print("file not exists!!!")
