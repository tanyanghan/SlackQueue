import logging
import logging.config
import json
import atexit
import SlackQueue
import Global
import time

time_program_start = time.time()
time_program_end = 0.0

def print_timing():
    time_slack_queue_finish = time.time()
    print ("Time taken by main program: %.5f"
                %(time_program_end - time_program_start))
    print ("Extra time taken by sending Slack messages: %.5f"
                %(time_slack_queue_finish - time_program_end))

#Load the logging config json file.
with open('Logger.json','r') as f:
    logging.config.dictConfig(json.load(f))

#Instantiate the queue listener with the same queue above, and also set
#the settings for communicating with Slack.
#You will need to get your own Incoming Webhook URL from Slack's Custom
#Integration setup.
SlackListener = SlackQueue.sqListener(
        Global.slack_queue,
        logging_url="https://hooks.slack.com/services/<your_webhook_url>",
        channel="#your_channel",
        username="Penguin",
        icon_emoji = ":penguin:"
    )

#Start the listener
SlackListener.start()

#Print out the timing measurement right at the end.
atexit.register(print_timing)

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

time_program_end = time.time()
