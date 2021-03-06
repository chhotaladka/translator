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
    self.url = "https://translate.google.com/#view=home&op=translate&sl=en&tl=hi"
    self.driver = None
    
    if lazy == False:
      self.driver = webdriver.Chrome(executable_path = os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=self.chrome_options)
      self.driver.get(self.url)

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      if self.driver == None:
        self.driver = webdriver.Chrome(executable_path = os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=self.chrome_options)
        self.driver.get(self.url)
      translation = ''
      try:
        #self.driver.get("https://translate.google.com/#view=home&op=translate&sl=en&tl=hi")
        src = self.driver.find_element_by_id("source")
        if src is not None:
          src.clear();
          src.send_keys(text)
          time.sleep(1)
          dest = self.driver.find_element_by_css_selector(".tlid-translation.translation")
          children = dest.find_elements_by_css_selector("*")
          for child in children:
            if (child.tag_name).lower() == 'span':
              translation += child.text
            elif (child.tag_name).lower() == 'br':
              translation += '\n'
      except:
          traceback.print_exc()
      #print(translation)
      return (translation)

  def __del__(self):
    if self.driver is not None:
      self.driver.quit()
