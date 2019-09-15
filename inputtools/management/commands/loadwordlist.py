from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from itertools import islice
from inputtools.models import Wordlist, BulkCreateManager
import os
import re
from django.conf import settings
import codecs


LANGUAGE = ['hi', 'en']


def findFilesInFolder(path, pathList, extension, subFolders=True):
    """  Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:        Base directory to find files
    pathList:    A list that stores all paths
    extension:   File extension to find
    subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    """

    try:  # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension):
                pathList.append(entry.path)
            elif entry.is_dir() and subFolders:  # if its a directory, then repeat process as a nested function
                pathList = findFilesInFolder(entry.path, pathList, extension, subFolders)
    except OSError:
        print('Cannot access ' + path + '. Probably a permissions error')

    return pathList


def pre_process(text):
    excludes = ',;[]{}().?@#$%^&*_+-"/\\|<>~`!'

    # word_num_eng = '01234569abcdefghijklmnopqrstuvwxyzABCDEFGZIJKLMNOPQRSTUVWZYZ'

    words = text.split();
    print(f"all word in file {len(words)}");
    # file_valid_words = len(words)
    # first get rid of english words
    words = [re.sub("[a-zA-Z]", "", w) for w in words]
    words = [re.sub("[0-9]", "", w) for w in words]
    words = [w.translate({ord(i): " " for i in excludes}) for w in words]
    words = [w.strip() for w in words]

    # special handling for ":"

    for word in words:
        if '\ufeff' in word:
            words.remove(word)
            break;

        for s in word:
            if s == ":":
                if len(word) == 1:
                    words.remove(word)
                    print(f" Invalid word {word}");
                    break
    words = [w for w in words if len(w) > 1]
    print(f"Valid words for file are : {len(words)}");
    return words


def find_all_words_resource():
    dir_name = settings.BASE_DIR + '/inputtools/resource/'
    print(f" BASE DIR for scanning is : {dir_name}");
    extension = ".txt"

    path_list = []

    path_list = findFilesInFolder(dir_name, path_list, extension, True)

    final_words = []
    for filename in path_list:
        print(f"reading file {filename}");
        with codecs.open(filename, encoding="utf-8", errors='ignore') as f:
            text = f.read()
            # This converts the encoded text to an internal unicode object, where
            # all characters are properly recognized as an entity:
            text = text

            word_list = pre_process(text)
            # print(word_list);
            final_words.extend(word_list);

    # print(final_words);
    print(f"Total unique words are {len(set(final_words))}");
    return set(final_words)


class Command(BaseCommand):
    """
    Load word lists in database from file
    """
    help = 'Load word lists in database from file'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('lang', help='language of the words to be loaded', choices=LANGUAGE, nargs='?', default='hi')
        parser.add_argument('filename', type=str, help='Name of file containing the words for particular lanuage', nargs='?', default="")

    def handle(self, *args, **options):
        # Access arguments inside **options dictionary
        language = options["lang"]
        filename = options["filename"]
        if len(filename) > 1:
            print(f"Parsing file {filename}");
            batch_size = 1000
            word_list = set()
            instances = BulkCreateManager(Wordlist)
            if os.path.exists(filename):
                with open(filename, encoding="utf8") as file1:
                    for line in file1:
                        words = line.split();
                        for w in words:
                            word_list.add(w);
                            obj = Wordlist(word=w, lang=language)
                            instances.append(obj);

                    print("total words parsed ", len(word_list));
                instances.create()
            else:
                print("file not exists!!!")
        else:
            print(f"No files passed scanning all files");
            words = find_all_words_resource();
            instances = BulkCreateManager(Wordlist)
            for word in words:
                obj = Wordlist(word=word, lang=language)
                instances.append(obj)

            instances.create();