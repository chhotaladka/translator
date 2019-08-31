import asyncio

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
