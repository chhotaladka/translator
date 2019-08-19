
class Client(object):
  def __init__(self, key=None, lazy=True):
    self.key = key


  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      translation = 'This is a dummy module!'
      return (translation)