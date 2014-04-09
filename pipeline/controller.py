'''
Controller script for the rabbitMQ consumers. rabbitMQ and worker settings defined in psettings.py.

This controller is also responsible for declaring the correct exchanges, queues, and bindings that its workers need.
'''

import os,sys
import importlib
import multiprocessing
import time
import signal
import pika

import psettings
import workers

#Do we continue to distribute this in lib?
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from lib import daemon

class RabbitMQConsumer:
  '''
  Base class that defines the necessary declare_* functions to communicate with rabbitMQ
  '''
  def __init__(self,params,*args,**kwargs):
    self.EXCHANGES = params['EXCHANGES']
    self.QUEUES = params['QUEUES']
    self.BINDINGS = params['BINDINGS']

  def connect(self,url,confirm_delivery=False):
    self.connection = pika.BlockingConnection(pika.URLParameters(url))
    self.channel = self.conn.channel()
    if confirm_delivery:
      self.channel.confirm_delivery()

  def declare_all(self):
    #todo: are these declarations blocking? Shouldn't matter either way, but would be nice to know.
    [self.channel.exchange_declare(**e) for e in self.EXCHANGES]
    [self.channel.queue_declare(**q) for q in self.QUEUES]
    [self.channel.queue_bind(**b) for b in self.BINDINGS]

def main():
  BaseConsumer = RabbitMQConsumer(psettings.RABBITMQ_SETTINGS)
  BaseConsumer.connect(psettings.RABBITMQ_URL)
  BaseConsumer.declare_all()
  BaseConsumer.connection.close()

  for worker,params in psettings.WORKERS.iteritems():
    params['RABBITMQ_URL'] = psettings.RABBITMQ_URL
    params['active'] = params.get('active',[])

    while len(params['active']) < params['concurrency']:
      parent_conn, child_conn = multiprocessing.Pipe()
      w = eval('workers.%s' % worker)(params,conn=child_conn)
      proc = multiprocessing.Process(target=w.run)
      proc.start()
      params['active'].append({
        'parent_conn':  parent_conn,
        'child_conn':   child_conn,
        'proc':         proc,
        })


if __name__ == '__main__':
  #with daemon.DaemonContext():
    main()