##############################################################################
# Source: https://www.geeksforgeeks.org/logging-in-python/
##############################################################################

import logging
from time import sleep
 
# Create and configure logger
logging.basicConfig(filename="./logs/dummy.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

print("press CTRL-C to stop...")

while (True):
    # Test messages
    logger.debug("Harmless debug Message")
    logger.info("Just an information")
    logger.warning("Its a Warning")
    logger.error("Did you try to divide by zero")
    logger.critical("Internet is down")
    logger.info("*************************************")
    print("sleep 5 sec...")
    sleep(5)