import logging
import subprocess as sb


def configure_logger(logger_name, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter('\n[%(asctime)s] [%(funcName)s] [%(levelname)s] %(message)s',
                                      datefmt='%d-%m-%Y %H:%M:%S')

    file_logger = logging.FileHandler(log_file)
    screen_logger = logging.StreamHandler()

    file_logger.setFormatter(log_formatter)
    screen_logger.setFormatter(log_formatter)

    logger.addHandler(file_logger)
    logger.addHandler(screen_logger)

    return logger


def auth_user_from_kerberos(userid, password):
    kinit_cmd = 'echo "%s" | /usr/bin/kinit %s@TOWER-RESEARCH.COM'\
        % (password, userid)
    get_token = "curl -s -c .ecmdb_cookie_%s.txt --negotiate  -u : " \
        "http://ecmdb.tower-research.com > /dev/null" % userid
    sb.call(kinit_cmd, shell=True)
    sb.call(get_token, shell=True)
    return
