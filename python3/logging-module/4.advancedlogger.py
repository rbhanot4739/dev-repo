# https://docs.python.org/3/howto/logging.html


def main():
    # Create the logger object
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)

    # create formatter object

    fileFormatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    consoleFormatter = logging.Formatter('%(name)s %(levelname)s %(message)s')

    # create the Handler object

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(consoleFormatter)

    fileHandler = logging.FileHandler(filename='main.log', mode='a')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(fileFormatter)

    logger.addHandler(fileHandler)
    logger.addHandler(ch)

    logger.debug('Debug msg')
    logger.info('Info msg')
    logger.warning('Warning msg')
    logger.error('Error msg')
    logger.critical('Critical Msg')


if __name__ == "__main__":
    import logging
    import mymath

    mymath.Main(5, 6)
    main()
