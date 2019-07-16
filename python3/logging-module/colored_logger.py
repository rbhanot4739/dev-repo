import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

consoleFormatter = logging.Formatter('%(name)s: %(levelname)s:   %(message)s')

ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
ch.setFormatter(consoleFormatter)

logger.addHandler(ch)


def print_log(logger, msg, level):
    reset = '\033[0m'
    yellow = '\033[93m'
    green = '\033[32m'
    orange = '\033[34m'
    lightred = '\033[91m'
    red = '\033[31m'
    COLORS = {'debug': yellow, 'info': green, 'warning': orange,
              'error': lightred, 'critical': red, 'reset': reset}
    getattr(logger, level)(COLORS[level] + msg + COLORS['reset'])


print_log(logger, 'Debug msg', 'debug')
print_log(logger, 'Info msg', 'info')
print_log(logger, 'Warning msg', 'warning')
print_log(logger, 'Error msg', 'error')
print_log(logger, 'Critical Msg', 'critical')