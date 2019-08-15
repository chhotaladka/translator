
import traceback
import time
import os

import socket
HOST,PORT = '127.0.0.1', 8888

class Client(object):
  def __init__(self, key=None):
    self.key = key
    self.translation = ''

  def translate(self, text=None, src_lang='en', dst_lang='hi'):
    if text is not None and len(text.strip()) > 0:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(text.strip().encode())
        self.translation = sock.recv(1024).decode()
        sock.close()
    return (self.translation)
