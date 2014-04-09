#!/usr/bin/env python
'''
Controller script for the main ADS import pipeline. Sends signals to controller.py, which is the parent of all the workers.
Usage:
  ADSimportpipeline.py status|start|stop|restart
'''

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from lib import daemon
#with daemon.DaemonContext():
  #do stuff
from lib import argparse
import psettings

COMMANDS = {}

def command(func):
  n = func.__name__
  COMMANDS[n] = func
  return func

@command
def status():
  pass

@command
def stop():
  print "stop"

@command
def start():
  print "start"

@command
def restart():
  stop()
  start()

def checkpid():
  pass

def main(argv=sys.argv):
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'command',
    help='|'.join([c for c in COMMANDS]),
    )
  args = parser.parse_args()
  if args.command not in COMMANDS:
    parser.error("Unknown command '%s'" % args.command)

  COMMANDS[args.command]()


if __name__ == '__main__':
  main()
