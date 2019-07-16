import logging, argparse, sys

parser = argparse.ArgumentParser(description='----- Set logging level -----')
parser.add_argument('--loglevel', help='Provide the desired log level from the list',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], required=True)
args = parser.parse_args()

loglevel = getattr(logging,
                   args.loglevel)  # Getting the value of log level from cmd and setting it through getattr function.
logFile = sys.argv[0].split('\\')[-1] + '.log'

logging.basicConfig(filename=logFile, level=loglevel, filemode='w', format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')

logging.debug('Setting the loglevel >= DEBUG will print Log messages of Debug & higher levels')
logging.info('Setting the loglevel >= INFO will print Log messages of INFO & higher levels')
logging.warning('Setting the loglevel >= WARNING will print Log messages of WARNING & higher  levels')
logging.error('Setting the loglevel >= ERROR will print Log messages of ERROR & higher levels')
logging.critical('Setting the loglevel = CRITICAL will print Log messages of only CRITICAL level')

with open(logFile, "rt") as f:
    logs = f.read()

print(logs)
