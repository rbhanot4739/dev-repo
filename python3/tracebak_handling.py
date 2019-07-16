import traceback
import sys
import logging



def divider(a, b):
    return a/b


def main(x, y):
    divider(x, y)


try:
    main(9, 0)
except Exception as e:
    logging.exception(e) # this will log the traceback to log handler.
    etype, evalue, tb = sys.exc_info()
    print(traceback.format_tb(tb))
    traceback.print_tb(tb)
