from google.cloud import translate
import os

class Client(object):
  def __init__(self, key=None, lazy=True):
    self.key = key
    if key is not None:
      os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key
    self.client = None
    if lazy == False:
      self.client = translate.Client()

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      if self.client == None:
        self.client = translate.Client()
      translation = self.client.translate(text, dst_lang)
      print(translation)
      return (translation['translatedText'])