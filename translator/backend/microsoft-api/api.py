import requests
import uuid
import json
import os

class Client(object):
  def __init__(self, key=None):
    self.key = key
    if key is not None:
      os.environ['MICROSOFT_APPLICATION_CREDENTIALS'] = key
    else:
      self.key = os.environ.get('MICROSOFT_APPLICATION_CREDENTIALS', None)

    if self.key is None:
        raise Exception("Translation engine key not configured.")
        print('Key not found')
    print('key: {a}'.format(a=self.key))



  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=hi'
    constructed_url = base_url + path + params
    headers = {
        'Ocp-Apim-Subscription-Key': self.key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    if text is not None and len(text.strip()) > 0:
      body = [{'text': text.strip()}]
      request = requests.post(constructed_url, headers=headers, json=body)
      response = request.json()
      translation = response[0].get("translations")[0]["text"]
      print(translation)
      return (translation)