from importlib import import_module
from .keys import keys
backends = {'google-api': 'google-api'}

class Engine(object):
  def __init__(self, engine='google-api'):
    self.backend = import_module('translator.backend.'+engine+'.api')
    self.client = self.backend.Client(key=keys.get(engine, None))

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    return self.client.translate(text, src_lang, dst_lang)