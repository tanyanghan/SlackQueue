import logging
import Queue as queue
import atexit
import sys
import SlackQueue

    
#Set up the root logger
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
root = logging.getLogger()

#Instantiate a queue for the handler/listener
slack_queue = queue.Queue(-1)

#Instantiate a queue handler using the queue above
SlackHandler = SlackQueue.sqHandler(slack_queue)
SlackHandler.setLevel("DEBUG")

#Set a formatter
simple = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
SlackHandler.setFormatter(simple)

#Add the queue handler to the root logger
root.addHandler(SlackHandler)

#Instantiate the queue listener with the same queue above, and also set
#the settings for communicating with Slack.
#You will need to get your own Incoming Webhook URL from Slack's Custom
#Integration setup.
SlackListener = SlackQueue.sqListener(
        slack_queue,
        logging_url="https://hooks.slack.com/services/<your_webhook_url>",
        channel="#your_channel",
        username="Penguin",
        icon_emoji = ":penguin:"
    )

#Start the listener
SlackListener.start()

#Register the listener stop method to run upon exit in order to allow the 
#queue to be emptied before exiting.
#If you miss this step, the queue might not be emptied before the program
#exits and you won't receive all the messages on Slack.
atexit.register(SlackListener.stop)


#Begin logging
logging.info("Test info message")

#You can temporarily change the Slack settings via the "extra" parameter.
#The settings in extra will only apply to this one log message.
logging.debug("Another test message",extra= {
                                                "channel":"@someone",
                                                "icon_emoji":":coffee:",
                                                "username":"Latte"
                                            })

#You can put the <!channel> tag in the message to send an announcement.
msg="Some sort of warning!"
logging.warning("<!channel>: %s"%msg)

logging.error("Gasp!")
