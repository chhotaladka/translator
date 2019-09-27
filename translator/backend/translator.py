from importlib import import_module
from .keys import keys

from django.core.cache import caches
from translator.keying import _smart_key

import socket
from nltk import tokenize

import re

cache = caches['default']

backends = {'dummy': 'dummy',
            'google-api': 'google-api',
            'google-selenium': 'google-selenium',
            'google-selenium-asyncio':'google-selenium-asyncio',
            'bing-selenium-asyncio':'bing-selenium-asyncio',
            'microsoft-api': 'microsoft-api',
            'bing-selenium': 'bing-selenium',
            'nmt': 'nmt'}


def check_internet(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    print(ex)
    return False

class Engine(object):
  def __init__(self, engine='microsoft-api'):
    if engine is not 'nmt':
      if (check_internet() == False):
        print('Internet not working. Fallback to offile tool')
        engine = 'nmt'
    self.backend = import_module('translator.backend.'+backends.get(engine, 'dummy')+'.api')
    self.client = self.backend.Client(key=keys.get(engine, None))

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    translation = ''
    paras = re.split("(.*\n?)",text);
    print('------------------------------------------');
    print(paras);
    print('------------------------------------------');
    ret = ""
    for p in paras:
      if len(p) > 0:
        sentences = tokenize.sent_tokenize(p)
        for s in sentences:
            translation = cache.get(_smart_key(s.strip()))
            if translation is None:
                print(f'Cache miss for {s}')
                translation = self.client.translate(s, src_lang, dst_lang)
                if len(translation) > 0:
                    cache.set(_smart_key(s.strip()), translation)
            else:
                print(f'Cache hit for {s}')
            ret += translation
      else:
        ret += '\n'
    return ret
