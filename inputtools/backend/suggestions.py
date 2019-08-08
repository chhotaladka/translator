from importlib import import_module

backends = {'dummy': 'dummy',
			'default': 'default'}

class Engine(object):
  def __init__(self, engine='default'):
    self.backend = import_module('inputtools.backend.'+backends.get(engine, 'default')+'.api')

  def suggest(self, text=None, lang='hi'):
    return self.backend.suggest(text, lang)