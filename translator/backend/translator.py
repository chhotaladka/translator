from importlib import import_module
from .keys import keys

from django.core.cache import caches
from translator.keying import _smart_key

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
    self.backend = import_module('translator.backend.'+backends.get(engine, 'dummy')+'.api')
    self.client = self.backend.Client(key=keys.get(engine, None))

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    translation = ''
    translation = cache.get(_smart_key(text.strip()))
    if translation is None:
        print('Cache miss')
        translation = self.client.translate(text, src_lang, dst_lang)
        cache.set(_smart_key(text.strip()), translation)
    else:
        print('Cache hit')

    return translation