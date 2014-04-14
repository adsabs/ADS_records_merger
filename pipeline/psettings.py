#Settings for the rabbitMQ/ADSimportpipeline


#The %2F is expected by pika if we connect to vhost="/"
#backpressure_detection is currently broken in pika(stable), but fixed in master.
#Push expected in 0.9.14 release
#see https://github.com/pika/pika/issues/347
#RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/%2F?backpressure_detection=t'
RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/%2F'

PIDFILE = '/tmp/ADSimportpipeline.lock'
POLL_INTERVAL = 3 #how many seconds to poll each worker to make sure it is alive.

RABBITMQ_ROUTES = {
  'EXCHANGES':[
    {
      'exchange': 'MergerPipelineExchange',
      'exchange_type': 'direct',
      'passive': False,
      'durable': True,
    },
  ],
  'QUEUES':[
    {
      'queue': 'FindNewRecordsQueue',
      'durable': True,
    },
    {
      'queue': 'UpdateRecordsQueue',
      'durable': True,
    },
    {
      'queue': 'MongoWriteQueue',
      'durable': True,
    },
  ],
  'BINDINGS':[
    {
      'queue':        'FindNewRecordsQueue',
      'exchange':     'MergerPipelineExchange',
      'routing_key':  'FindNewRecordsRoute',
    },
    {
      'queue':        'UpdateRecordsQueue',
      'exchange':     'MergerPipelineExchange',
      'routing_key':  'UpdateRecordsRoute',
    },
    {
      'queue':        'MongoWriteQueue',
      'exchange':     'MergerPipelineExchange',
      'routing_key':  'MongoWriteRoute',
    },  
  ],
}

WORKERS = {
  'FindNewRecordsWorker': { 
    'concurrency': 1,
    'qos_prefetch': 10,
    'publish': [
      {'exchange': 'MergerPipelineExchange', 'routing_key': 'UpdateRecordsRoute',},
    ],
    'subscribe': [
      {'queue': 'FindNewRecordsQueue',},
    ],
  },

  'UpdateRecordsWorker': {
    'concurrency': 1,
    'qos_prefetch': 10,
    'publish': [
      {'exchange': 'MergerPipelineExchange','routing_key': 'MongoWriteRoute',},
    ],
    'subscribe': [
      {'queue': 'FindNewRecordsQueue',},
    ],
  },
  
  'MongoWriteWorker': {
    'concurrency': 1,
    'qos_prefetch': 10,
    'publish': [],
    'subscribe': [
      {'queue':'FindNewRecordsQueue',},
    ],
  },
}