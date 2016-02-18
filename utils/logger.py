import logging

logger = logging.getLogger('duty-notify')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s / %(levelname)s] %(message)s',
    '%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
