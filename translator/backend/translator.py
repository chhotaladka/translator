from importlib import import_module
from .keys import keys

from django.core.cache import caches
from translator.keying import _smart_key

import urllib.request
from nltk import tokenize

cache = caches['default']

backends = {'dummy': 'dummy',
            'google-api': 'google-api',
            'google-selenium': 'google-selenium',
            'google-selenium-asyncio':'google-selenium-asyncio',
            'microsoft-api': 'microsoft-api',
            'bing-selenium': 'bing-selenium',
            'nmt': 'nmt'}

class Engine(object):
  def __init__(self, engine='microsoft-api'):
    if engine is not 'nmt':
      if (urllib.request.urlopen("https://google.com/").getcode() != 200):
        print('Internet not working. Fallback to offile tool')
        engine = 'nmt'
    self.backend = import_module('translator.backend.'+backends.get(engine, 'dummy')+'.api')
    self.client = self.backend.Client(key=keys.get(engine, None))

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    translation = ''
    sentences = tokenize.sent_tokenize(text)
    ret = ""
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
    return ret
