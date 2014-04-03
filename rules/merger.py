import sys,os
from rules.settings import MERGER_RULES
import settings
print dir(settings)
sys.exit()
import types

def dispatcher(f1,f2,fieldName,*args,**kwargs):
  '''
  Provides a first order security for string mappings via eval()
  '''
  assert(f1['@origin'])
  assert(f2['@origin'])

  if fieldName not in MERGER_RULES:
    fieldName = 'default'

  if type(MERGER_RULES[fieldName])==types.FunctionType:
    return MERGER_RULES[fieldName](f1,f2,fieldName, *args, **kwargs)
  else:
    #Assert that the string maps to function defined within this module
    assert type(eval(MERGER_RULES[fieldName]))==types.FunctionType
    assert MERGER_RULES[fieldName] in dir(sys.modules[__name__])

    return eval(MERGER_RULES[fieldName])(f1,f2,fieldName,*args,**kwargs)


def takeAll(f1,f2,*args,**kwargs):
  #takeAll merger only makes sense with lists.
  #Remember: Understand why the previous merger compared trust values here
  assert type(f1['content']==list)
  assert type(f2['content']==list)
  return list( set(f1['content']).union(f2['content']) )

def stringConcatenateMerger(f1,f2,*args,**kwargs):
  return "<%s><%s>" % (f1,f2)


def authorMerger(f1,f2,*args,**kwargs):
  pass
def pubdateMerger(f1,f2,*args,**kwargs):
  pass

def referencesMerger(f1,f2,*args,**kwargs):
  assert type(f1['content']==list)
  assert type(f2['content']==list)


def originTrustMerger(f1,f2,tag,*args,**kwargs):
  pass
def fallbackMerger(f1,f2,*args,**kwargs):
  pass