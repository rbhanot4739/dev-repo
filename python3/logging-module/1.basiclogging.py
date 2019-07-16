import logging, time

logging.basicConfig(level=logging.INFO)

logging.info(' Test INFO entry at {}'.format(
    time.ctime(time.time())))  # This will not be printed as the default logging level is Warning
logging.warning(' Test WARNING entry at {}'.format(time.ctime(time.time())))
