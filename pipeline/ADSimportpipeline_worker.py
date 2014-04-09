'''
Controller script for the rabbitMQ consumers. rabbitMQ and worker settings defined in psettings.py.
'''

import os,sys
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

import multiprocessing

#Do we continue to distribute this in lib?
from lib import daemon
import psettings
import workers



def main():
  WORKERS = psettings.WORKERS
  for worker,params in WORKERS.iteritems():
    params['active'] = params.get('active',[])
    while len(params['active']) < params['concurrency']:
      parent_conn, child_conn = multiprocessing.Pipe()
      w = eval('workers.%s' % worker)(conn=child_conn,**params)
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