def Main(a, b):
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(filename='main.log', mode='w')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    def add(x, y):
        return x + y

    def mul(x, y):
        return x * y

    def div(x, y):
        try:
            res = x / y
        except ZeroDivisionError as e:
            logger.exception(e)
        else:
            return res

    logger.debug('{} + {} = {}'.format(a, b, add(a, b)))
    logger.debug('{} * {} = {}'.format(a, b, mul(a, b)))
    logger.debug('{} / {} = {}'.format(a, b, div(a, b)))


if __name__ == "__main__":
    Main(5, 0)
