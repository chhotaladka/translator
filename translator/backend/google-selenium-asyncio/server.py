import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import traceback
import time
import os

import signal

loop = None
driver = None
server = None

def handler(signum, frame):
  print('Shutting down...')
  if driver is not None:
    driver.close()
    driver.quit()
  if server is not None and loop is not None:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
  import sys
  sys.exit(0)

def translate(driver, text=None):
    if text is not None and len(text.strip()) > 0:
      translation = ''
      try:
        src = driver.find_element_by_id("source")
        if src is not None:
          src.clear();
          src.send_keys(text)
          time.sleep(0.9)
          dest = driver.find_element_by_css_selector(".tlid-translation.translation")
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


class EchoServerClientProtocol(asyncio.Protocol):
  def __init__(self, driver, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.driver = driver
    self.terminate = False

  def connection_made(self, transport):
    peername = transport.get_extra_info('peername')
    print('Connection from {}'.format(peername))
    self.transport = transport

  def data_received(self, data):
    message = data.decode()
    print('Data received: {!r}'.format(message))

    translation = translate(self.driver, message)

    print('Send: {!r}'.format(translation))
    self.transport.write(translation.encode('utf-8'))

    print('Close the client socket')
    self.transport.close()

def main():
  global loop
  global server
  global driver

  signal.signal(signal.SIGTERM, handler)

  chrome_options = Options()
  chrome_options.add_argument('--headless')
  #chrome_options.binary_location='/opt/google/chrome/google-chrome'
  driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=chrome_options)
  try:
    driver.get("https://translate.google.com/#view=home&op=translate&sl=en&tl=hi")
  except:
      traceback.print_exc()
      driver.close()
      driver.quit()
  #loop = asyncio.get_event_loop()
  try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    coro = loop.create_server(lambda:EchoServerClientProtocol(driver), '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)
    print('Serving on {}'. format(server.sockets[0].getsockname()))
    try:
      loop.run_forever()
    except KeyboardInterrupt:
      pass

    try:
      driver.close()
      driver.quit()
      server.close()
      loop.run_until_complete(server.wait_closed())
      loop.close()
    except:
      traceback.print_exc()
  except OSError:
      print('Quitting thread')
      driver.close()
      driver.quit()

if __name__ == '__main__':
  main()
