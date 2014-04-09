import os,sys
import time
import pika
from controller import RabbitMQConsumer

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from lib import utils




class FindNewRecordsWorker(RabbitMQConsumer):
  def __init__(self,params,*args,**kwargs):
    self.connect(params['RABBITMQ_URL'])

  def run(self):
    print self.__class__.__name__

class UpdateRecordsWorker(RabbitMQConsumer):
  def __init__(self,params,*args,**kwargs):
    pass
  def run(self):
    print self.__class__.__name__  

class MongoWriteWorker(RabbitMQConsumer):
  def __init__(self,params,*args,**kwargs):
    pass
  def run(self):
    print self.__class__.__name__
    time.sleep(10)    