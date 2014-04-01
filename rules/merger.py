import sys,os
from settings import MERGER_RULES
import types
from ..settings import LOGGER

def dispatcher(f1,f2,tag,*args,**kwargs):
  '''
  Provides a first order security for string mappings via eval()
  '''

  if type(MERGER_RULES[tag])==types.FunctionType:
    return MERGER_RULES[tag](f1,f2,tag)
  else:
    #Assert that the string maps to function defined within this module
    assert type(eval(MERGER_RULES[tag]))==types.FunctionType
    assert MERGER_RULES[tag] in dir(sys.modules[__name__])

    return eval(MERGER_RULES[tag](f1,f2,tag))


def takeAll(f1,f2,*args,**kwargs):
  #takeAll merger only makes sense with lists.

  #Remember: Understand why the previous merger compared trust values here
  assert(type(f1)==list and type(f2)==list)
  return list( set(f1).union(f2) )

def priorityMerger(f1,f2,*args,**kwargs):
  pass
def abstractMerger(f1,f2,*args,**kwargs):
  pass
def titleMerger(f1,f2,*args,**kwargs):
  pass
def authorMerger(f1,f2,*args,**kwargs):
  pass
def pubdateMerger(f1,f2,*args,**kwargs):
  pass
def referencesMerger(f1,f2,*args,**kwargs):
  pass


def _rankTrust(f1,f2,tag,*args,**kwargs):
  pass

def _getBestFields(f1,f2,*args,**kwargs):