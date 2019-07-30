from importlib import import_module
from .keys import keys

backends = {'dummy': 'dummy',
            'google-api': 'google-api',
            'google-selenium': 'google-selenium',
            'google-selenium-asyncio':'google-selenium-asyncio'}

class Engine(object):
  def __init__(self, engine='google-selenium-asyncio'):
    self.backend = import_module('translator.backend.'+backends.get(engine, 'dummy')+'.api')
    self.client = self.backend.Client(key=keys.get(engine, None))

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    return self.client.translate(text, src_lang, dst_lang)