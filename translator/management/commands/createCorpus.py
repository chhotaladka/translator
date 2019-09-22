from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from itertools import islice
from translator.backend import translator
from translator.settings import translator_settings

import os
import re
from django.conf import settings
import codecs


LANGUAGE = ['hi', 'en']


class Command(BaseCommand):
    """
    Load word lists in database from file
    """
    help = 'create parallel corpus of English and Hindi by reading English from file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='?', help='Name of file containing English words', type=str, default="")
        parser.add_argument('batch', nargs='?', help='Batch of lines to write in file', type=int, default=1000)

    def handle(self, *args, **options):
        # Access arguments inside **options dictionary
        filename = options["filename"]
        batch_size = options["batch"]
        if len(filename) > 1:
            print(f"Parsing file {filename}");
            eng_list = []
            hindi_list = []
            num_batches = 0;
            engine = translator.Engine(engine=translator_settings.BACKEND)
            if os.path.exists(filename):
                with open(filename, encoding="utf8") as file1:
                    for line in file1:
                      if len(line) > 0:
                        translation = engine.translate(line.strip())
                        if len(translation) > 0:
                          hindi_list.append(translation);
                          eng_list.append(line);
                          if len(eng_list) >= batch_size:
                            num_batches +=1;
                            print("WRITING BATCH " + str(num_batches));
                            with open('train.en', 'a+') as a, open('train.hi', 'a+') as b:
                              a.write("".join(eng_list));
                              b.write("\n".join(hindi_list));
                              eng_list.clear();
                              hindi_list.clear();
                    # check if some lines are remained in list
                    if len(eng_list) > 0:
                      with open('train.en', 'a+') as a, open('train.hi', 'a+') as b:
                        a.write("".join(eng_list));
                        b.write("\n".join(hindi_list));



            else:
                print("file not exists!!!")
        else:
            print(f"No file passed Error");
            