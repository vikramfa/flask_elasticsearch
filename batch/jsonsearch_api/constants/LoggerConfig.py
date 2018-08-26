import inspect
import logging
import os
class ClassLoggers:

    def function_logger(self, file_level, console_level = None, funcName=None):
        #function_name = inspect.stack()[1][3]
        logDir = os.environ['LOG_DIR']
        logger = logging.getLogger(funcName)
        logger.setLevel(logging.DEBUG) #By default, logs all messages

        if console_level != None:
            ch = logging.StreamHandler() #StreamHandler logs to console
            ch.setLevel(console_level)
            ch_format = logging.Formatter('%(asctime)s - %(message)s')
            ch.setFormatter(ch_format)
            logger.addHandler(ch)

        fh = logging.FileHandler(os.path.join(logDir,"webApps.log"))
        fh.setLevel(file_level)
        fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(filename)s - %(funcName)s - %(message)s')
        fh.setFormatter(fh_format)
        logger.addHandler(fh)

        return logger

    def f3(self):
        f3_logger = self.function_logger(logging.DEBUG, logging.DEBUG)
        f3_logger.debug('application started')



def main():
    logger = ClassLoggers()
    logger.f3()
    #logger.f2()
    #logging.shutdown()

main()