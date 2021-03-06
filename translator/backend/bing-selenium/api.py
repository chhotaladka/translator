from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import traceback
import time
import os

class Client(object):
  def __init__(self, key=None, lazy=True):
    self.key = key
    self.chrome_options = Options()
    self.chrome_options.add_argument('--headless')
    self.url = "https://www.bing.com/translator?from=en&to=hi"
    self.driver = None
    if lazy==False:
      self.driver = webdriver.Chrome(executable_path = os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=self.chrome_options)
      self.driver.get(self.url)

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      if self.driver==None:
        self.driver = webdriver.Chrome(executable_path = os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=self.chrome_options)
        self.driver.get(self.url)
      translation = ''
      try:
        src = self.driver.find_element_by_id("tta_input")
        if src is not None:
          src.clear();
          src.send_keys(text)
          time.sleep(1)
          dest = self.driver.find_element_by_id("tta_output")
          translation = dest.get_attribute('value')

      except:
          traceback.print_exc()
      #print(translation)
      return (translation)

  def __del__(self):
    self.driver.quit()
