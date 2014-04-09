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
from workers import RabbitMQConsumer

#Do we continue to distribute this in lib?
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from lib import daemon


def main():

  #Make sure the plumbing in rabbitMQ is correct; this procedure is idempotent
  BaseConsumer = RabbitMQConsumer()
  BaseConsumer.connect(psettings.RABBITMQ_URL)
  BaseConsumer.declare_all(*[psettings.RABBITMQ_SETTINGS[i] for i in ['EXCHANGES','QUEUES','BINDINGS']])
  BaseConsumer.connection.close()


  for worker,params in psettings.WORKERS.iteritems():
    params['active'] = params.get('active',[])
    params['RABBITMQ_URL'] = psettings.RABBITMQ_URL
    
    while len(params['active']) < params['concurrency']:
      #parent_conn, child_conn = multiprocessing.Pipe()
      w = eval('workers.%s' % worker)(params)
      proc = multiprocessing.Process(target=w.run)
      proc.start()
      params['active'].append({
        'proc': proc,
        })


if __name__ == '__main__':
  #with daemon.DaemonContext():
    main()