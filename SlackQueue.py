from logging import Handler
import requests
import json
#QueueHandler and QueueListener is part of standard Python logging module
#from Python 3.2 onwards; but if you're using Python 2.x, you can just 
#copy the QueueHandler and QueueListener code and save it into your own 
#queueHandler.py.
try:
    #check if they're part of standard Python logging module
    from logging.handlers import QueueHandler
    from logging.handlers import QueueListener
except ImportError:
    #if not, use your own copy
    from queueHandler import QueueHandler
    from queueHandler import QueueListener


class sqHandler(QueueHandler):
    def __init__(self, queue=None):
        QueueHandler.__init__(self,queue)

    def prepare(self, record):
        """
        Override the method to allow the formatter to work.
        """
        record.msg = self.format(record)
        record.args = None
        record.exc_info = None
        return record

class sqListener(QueueListener,Handler):
    def __init__(self, queue=None, logging_url="", channel="", username="",
                 icon_emoji = ""):
        QueueListener.__init__(self,queue)
        Handler.__init__(self)
        """
        logging_url, channel, username, icon_emoji can all be overridden
        by the extra dictionary parameter of a logging record
        For example: 
            logging.info('Test messate',extra={'channel':'@someone',
                                               'username':'testbot',
                                               'icon_emoji':':penguin:'})
        """
        self.logging_url = logging_url
        self.payload = {
            "channel": channel,
            "username": username,
            "icon_emoji": icon_emoji
            }

    def handle(self, record):
        """
        Override the QueueListener.handle method with the Handler.handle 
        method
        """
        Handler.handle(self, record)

    def emit(self, record):
        #make a copy of the default settings
        new_logging_url = self.logging_url
        new_payload = self.payload.copy()

        #override default settings if necessary
        if hasattr(record,'logging_url'):
            new_logging_url = record.logging_url

        for key in self.payload.keys():
            if hasattr(record,key):
                new_payload[key] = record.__dict__[key]
                del record.__dict__[key]

        #format the message and add to payload
        msg = self.format(record)
        new_payload["text"] = '%s' % msg

        #post the request
        requests.post(new_logging_url, data=json.dumps(new_payload))
