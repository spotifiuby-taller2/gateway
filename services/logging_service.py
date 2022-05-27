import logging
import datetime

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def logInfo(msg):
    timestamp = str(datetime.datetime.now()).split('.')[0] + ' - '
    logging.info(timestamp + msg)
