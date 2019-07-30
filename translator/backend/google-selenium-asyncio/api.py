
import traceback
import time
import os

import asyncio

class ClientProtocol(asyncio.Protocol):
  def __init__(self, client, message, loop):
    self.message = message
    self.loop = loop
    self.client = client

  def connection_made(self, transport):
    transport.write(self.message.encode())
    print('Data sent: {!r}'.format(self.message))

  def data_received(self, data):
    print('Data received: {!r}'.format(data.decode()))
    self.client.translation = data.decode()

  def connection_lost(self, exc):
    print('The server closed the connection')
    print('Stop the event loop')
    self.loop.stop()


class Client(object):
  def __init__(self, key=None):
    self.key = key
    self.translation = ''

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      loop = asyncio.new_event_loop()
      #loop = asyncio.get_event_loop()
      asyncio.set_event_loop(loop)
      coro = loop.create_connection(lambda: ClientProtocol(self, text.strip(), loop), '127.0.0.1', 8888)

      loop.run_until_complete(coro)
      loop.run_forever()
      loop.close()
    return (self.translation)
