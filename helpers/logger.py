import logging


def get_logger(name):
    logger logging.getLogger(name)
    if not logger.hasHandlers():
      logger.setLevel(logging.INFO) #Set the logging level to ERROR
      handler logging.StreamHandler()
      formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s %(message)s')
      handler.setFormatter (formatter)
      Logger.addHandler (handler)
    return logger
