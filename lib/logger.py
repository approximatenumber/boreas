import logging

class Logger:
    handler = logging.StreamHandler()
    _format = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    handler.setFormatter(_format)

    @classmethod
    def get_logger(cls, name, loglevel=logging.INFO):
        logger = logging.getLogger(name)
        logger.addHandler(cls.handler)
        logger.setLevel(loglevel)
        logger.propagate = False  # See: https://stackoverflow.com/questions/6729268/log-messages-appearing-twice-with-python-logging
        return logger
