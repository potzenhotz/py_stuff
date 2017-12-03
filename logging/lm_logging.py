#!/usr/bin/env python
import logging
import datetime as dt
import sys
 
 
#-----------------------------------------------------------------------
# Logging
#-----------------------------------------------------------------------
class simple_logging(object):
    """
    Class for easy logging
    1)DEBUG 2)INFO 3)WARNING(Default) 4)ERROR 5)CRITICAL
    """
 
    def __init__(self):
        """
        Sets inital logging opject with defined formater
        """
        self.logging = logging
        self.logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
        self.rootLogger = logging.getLogger()
        self.rootLogger.setLevel(logging.DEBUG)
 
    def set_logfile(self, logPath='.', logFileName='logfile', mode='w'):
        """
        Sets a logfile where log messages are dumped
        3 Inputs can be defined
        """
        self.fileHandler = logging.FileHandler("{0}/{1}_{2}.log".format(logPath,
logFileName,dt.datetime.now().strftime("%Y%m%d-%H%M%S")), mode='w')
        self.fileHandler.setFormatter(self.logFormatter)
        self.rootLogger.addHandler(self.fileHandler)
 
    def set_console(self):
        """
        Dumps logging messages to the console
        """
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(self.logFormatter)
        self.rootLogger.addHandler(self.consoleHandler)
 
#Decorator for functions
def handle_exceptions(f):
    """
    A wrapper for try/exception handling
    """
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            logging.critical("Function {0} failed with error {1}".format(f.__name__, e))
            #logging.debug("Function {0} failed with error {1}".format(inspect.stack(), e))
            sys.exit()
    return wrapper
 
 
 
 
 
#-----------------------------------------------------------------------
#This part will only be executed if the logging module is used directly
#-----------------------------------------------------------------------
if __name__ == "__main__":
    #-----------------------------------------------------------------------
    # Intialiaze logging
    #-----------------------------------------------------------------------
    log = simple_logging()
    log.set_logfile()
    log.set_console()
    logger = log.rootLogger
    #logger.setLevel(log.logging.ERROR)
    logger.setLevel(log.logging.INFO)
    #logger.setLevel(log.logging.DEBUG)
 
    #-----------------------------------------------------------------------
    # How to use logging
    #-----------------------------------------------------------------------
 
    #Log a simple message with severity info
    logger.info('Starting simple logging')
 
    try:
        #Log a simple message with severity info
        logger.info('Hello World!')
    except:
        #Log a error message with severity error
        logger.error('Could not print "Hello World!"')
 
    dummy_string = 'Hello World!'
    #Log all variables which are defined
    for name in dir():
        if not name.startswith('__'):
            myvalue = eval(name)
            logger.info('VARIABLES: {0} is {1} and is equal to: "{2}"'.format(name, type(myvalue), myvalue))
 
    #Wrap try/except handling aroung a function
    @handle_exceptions
    def succeed_function():
        """
        Dumb routine which which does not fail...
        """
        print('succeed_function succeeded')
 
    #Wrap try/except handling aroung a function
    @handle_exceptions
    def fail_function():
        """
        Dumb routine which which fails...
        """
        integer = int("A")
 
    succeed_function()
    fail_function()
