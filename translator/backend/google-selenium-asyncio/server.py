import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import traceback
import time
import os

import signal
import functools


server = None


from queue import Empty, Queue
from threading import Thread

num_threads = 2

q = None
workers = []

RELOAD_AFTER = 10

def shutdown():
  global q
  global workers
  global server

  print('Shutting down...')
  if len(workers)>0:
      for i in range(num_threads):
        q.put('stop')
      try:
        while True:
            worker_thread = workers.pop()
            worker_thread.join()
      except IndexError:
        pass


  if server is not None:
    server.close()
    server = None
    #loop.stop()
    #loop.wait_closed()
    #loop.close()

def handler(signum):
    print('Signal handled.')
    shutdown()

def translate(driver, text=None, wait=0.9):
    if text is not None and len(text.strip()) > 0:
      translation = ''
      try:
        src = driver.find_element_by_id("source")
        if src is not None:
          src.clear();
          src.send_keys(text)
          time.sleep(wait)
          dest = driver.find_element_by_css_selector(".tlid-translation.translation")
          children = dest.find_elements_by_css_selector("*")
          for child in children:
            if (child.tag_name).lower() == 'span':
              translation += child.text
            elif (child.tag_name).lower() == 'br':
              translation += '\n'
        retry=False
      except:
          traceback.print_exc()
          retry = True
      #print(translation)
      return (translation, retry)


class EchoServerClientProtocol(asyncio.Protocol):
  def __init__(self, queue, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.queue = queue
    self.terminate = False

  def connection_made(self, transport):
    peername = transport.get_extra_info('peername')
    print('Connection from {}'.format(peername))
    self.transport = transport

  def data_received(self, data):
    print('data received')
    self.message = data.decode()
    print('Data received: {!r}'.format(self.message))
    self.translation = ''
    self.queue.put(self)

  def send_response(self):
    print('Send: {!r}'.format(self.translation))
    self.transport.write(self.translation.encode('utf-8'))

    print('Close the client socket')
    self.transport.close()

def worker(name, queue):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    retry_count = 0
    #chrome_options.binary_location='/opt/google/chrome/google-chrome'
    try:
        driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__))+"/../resources/chromedriver", chrome_options=chrome_options)
        driver.get("https://translate.google.com/#view=home&op=translate&sl=en&tl=hi")

        while True:
            try:
                work = queue.get(timeout=0.1)
                if isinstance(work, EchoServerClientProtocol):
                    retry_count += 1
                    (work.translation, retry )= translate(driver, work.message, wait=0.9)
                    if(retry is True):
                        driver.get("https://translate.google.com/#view=home&op=translate&sl=en&tl=hi")
                        (work.translation, retry )= translate(driver, work.message, wait=0.9)
                    work.send_response()
                    if(retry_count%RELOAD_AFTER == 0):
                        retry_count = 0
                        driver.get("https://translate.google.com/#view=home&op=translate&sl=en&tl=hi")


                elif isinstance(work, str):
                    if work=='stop':
                        break;
                queue.task_done()
            except Empty:
                pass

        print('Closing {a}'.format(a=name))
        #driver.close()
        driver.quit()

    except:
        traceback.print_exc()


def main(ip='127.0.0.1', port=10000):
  global loop
  global server
  global coro
  global q
  global workers

  try:
    q = Queue(num_threads)

    for i in range(num_threads):
        name='T-{i}'.format(i=i)
        worker_thread = Thread(target=worker, args=(name, q))
        worker_thread.start()
        workers.append(worker_thread)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for signame in ('SIGINT', 'SIGTERM'):
      loop.add_signal_handler(getattr(signal, signame),
                            functools.partial(handler, signame))
    coro = loop.create_server(lambda:EchoServerClientProtocol(q), ip, port)
    server = loop.run_until_complete(coro)
    print('Serving on {}'. format(server.sockets[0].getsockname()))
    try:
      #loop.run_forever()
      loop.run_until_complete(server.wait_closed())
      print("Moving on")
    except KeyboardInterrupt:
      pass

    try:
      shutdown()
      loop.close()

    except:
      traceback.print_exc()
  except OSError:
      print('Quitting thread')
      for i in range(num_threads):
          q.put('stop')
      try:
        while True:
            worker_thread = workers.pop()
            worker_thread.join()
      except IndexError:
        pass
      traceback.print_exc()

if __name__ == '__main__':
  import sys
  if len(sys.argv)==2:
    main(sys.argv[0], sys.argv[1])
  else:
    main()
