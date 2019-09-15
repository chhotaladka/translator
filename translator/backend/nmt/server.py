import asyncio
import traceback
import time
import os
import signal
import functools
from queue import Empty, Queue
from threading import Thread
from django.conf import settings
from .tf_nmt import tf_nmt
from .protocol import EchoServerClientProtocol
import numpy as np
import tensorflow as tf
from .tf_nmt import inference
from .tf_nmt.utils import misc_utils as utils
from .tf_nmt.utils import vocab_utils
import sys
from importlib import import_module

server = None

FLAGS = None

# Number of threads FIXME get it from setting
num_threads = 1

# queue
q = None

# List of workers
workers = []

def shutdown():
  """
  This function would be called on shutdown
  """
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


def handler(signum):
  """
  Handle signal 
  """
  print('Signal handled.')
  shutdown()

def worker(name, queue):

    # Call NMT function here which in turn will call tf.compat.v1.app.run
    # FIXME listen on queue on that function
    try:
      # tf_nmt.start_nmt_thread(queue)
      default_hparams = tf_nmt.create_hparams(FLAGS)
      inference_fn = inference.quick_inference
      tf_nmt.run_main(FLAGS, queue, default_hparams, inference_fn)

      print('Closing {a}'.format(a=name))
    except:
        traceback.print_exc()

def start_nmt_thread(ip='127.0.0.1', port=10000):
  global FLAGS
  global server
  global q
  global workers

  try:
    q = Queue(num_threads)

    FLAGS = tf_nmt.Hparam()
    settings = import_module('demo.settings')
    FLAGS.out_dir = settings.BASE_DIR + '/translator/backend/resources/nmt_model'
    # FLAGS.hparams_path = '/home/abhishek/nmt-master/standard_hparams/wmt16_gnmt_8_layer.json'
    tf.compat.v1.app.run(main=main, argv=[q])

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



def main(args):
  global FLAGS
  global workers
  for i in range(num_threads):
      name='T-{i}'.format(i=i)
      worker_thread = Thread(target=worker, args=(name, args[0]))
      worker_thread.start()
      workers.append(worker_thread)
  




# def main(ip='127.0.0.1', port=10000):
#   global server
#   global q
#   global workers

#   try:
#     q = Queue(num_threads)

#     for i in range(num_threads):
#         name='T-{i}'.format(i=i)
#         worker_thread = Thread(target=worker, args=(name, q))
#         worker_thread.start()
#         workers.append(worker_thread)

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     for signame in ('SIGINT', 'SIGTERM'):
#       loop.add_signal_handler(getattr(signal, signame),
#                             functools.partial(handler, signame))
#     coro = loop.create_server(lambda:EchoServerClientProtocol(q), ip, port)
#     server = loop.run_until_complete(coro)
#     print('Serving on {}'. format(server.sockets[0].getsockname()))
#     try:
#       #loop.run_forever()
#       loop.run_until_complete(server.wait_closed())
#       print("Moving on")
#     except KeyboardInterrupt:
#       pass

#     try:
#       shutdown()
#       loop.close()

#     except:
#       traceback.print_exc()
#   except OSError:
#       print('Quitting thread')
#       for i in range(num_threads):
#           q.put('stop')
#       try:
#         while True:
#             worker_thread = workers.pop()
#             worker_thread.join()
#       except IndexError:
#         pass
#       traceback.print_exc()

if __name__ == '__main__':
  import sys
  if len(sys.argv)==2:
    main(sys.argv[0], sys.argv[1])
  else:
    main()
