import logging, sys

logFile = sys.argv[0].split('\\')[-1] + '.log'
logging.basicConfig(filename=logFile, level=logging.DEBUG, format='%(levelname)s:%(message)s', filemode='w',
    # This will open the log file in write 'w' mode. The default mode is append 'a'
)

logging.debug('This is a debug log entry')
logging.info('This is a info log entry')
logging.warning('This is a warning log entry')

with open(logFile, "rt") as f:
    print(f.read())
